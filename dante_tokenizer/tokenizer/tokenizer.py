import argparse
import regex
import html

from nltk import tokenize

from dante_tokenizer.data.load import read_test_data
from dante_tokenizer.evaluate import evaluate_dataset
from dante_tokenizer.data.preprocessing import expand_contractions, split_monetary_tokens, normalize_text

#region Regex definitions

# This particular element is used in a couple ways, so we define it
# with a name:
EMOTICONS = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']*                 # optional nose
      [\)\]+\(\[dDpPoO/\:\}\{@\|\\]+ # mouth
      |
      [\)\]+\(\[dDpPoO/\:\}\{@\|\\]+ # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
      |
      (?:\b[oO].[oO]\b)          # O.o O.o o.o O.O
      |
      (?:,\))
      |
      (?:\*+(?:-|\.)\*+)
      |
      <3                         # heart
    )"""

# URL pattern due to John Gruber, modified by Tom Winzig. See
# https://gist.github.com/winzig/8894715

URLS = r"""			# Capture 1: entire matched URL
  (?:
  https?:				# URL protocol and colon
    (?:
      /{1,3}				# 1-3 slashes
      |					#   or
      [a-z0-9%]				# Single letter or digit or '%'
                                       # (Trying not to match e.g. "URI::Escape")
    )
    |					#   or
                                       # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:[a-z]{2,13})
    /
  )
  (?:					# One or more:
    [^\s()<>{}\[\]]+			# Run of non-space, non-()<>{}[]
    |					#   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\) # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)				# balanced parens, non-recursive: (...)
  )+
  (?:					# End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\) # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)				# balanced parens, non-recursive: (...)
    |					#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]	# not a space or one of these punct chars
  )
  |					# OR, the following to match naked domains:
  (?:
  	(?<!@)			        # not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:[a-z]{2,13})
    \b
    /?
    (?!@)			        # not succeeded by a @,
                            # avoid matching "foo.na" in "foo.na@example.com"
  )
"""

# The components of the tokenizer:
REGEXPS = (
    URLS,
    # Phone numbers:
    #r"""
    #(?:
    #  (?:            # (international)
    #    \+?[01]
    #    [ *\-.\)]*
    #  )?
    #  (?:            # (area code)
    #    [\(]?
    #    \d{3}
    #    [ *\-.\)]*
    #  )?
    #  \d{3}          # exchange
    #  [ *\-.\)]*
    #  \d{4}          # base
    #)""",
    # ASCII Emoticons
    EMOTICONS,
    # HTML tags:
    r"""<[^>\s]+>""",
    # ASCII Arrows
    r"""[\-]+>|<[\-]+""",
    # Twitter username:
    r"""(?:@[\w_]+)""",
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)""",
    # email addresses
    r"""[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]""",
    # Remaining word types:
    r"""
    (?:\b[\w]{4}-[\w]{1,2}\b) # lren-nm elet-n1
    |
    (?:\b[a-zA-Z]{3,5}-?[\d]{1}\b) # JSB-3 Eletr6
    |
    \b(?:[a-zA-Z]\.){2,} # Acronyms like: J.B.S.A
    |
    (?:\w)+\&(?:\w)+ # S&P BMF&Bovespa
    |
    # Datas nos formatos DD/MM/AAAA, DD/MM, DD-MM-AAAA, DD.MM.AAAA
    \b(?:\d{1,2}|(?:(?i)jan(?:eiro)?|fev(?:ereiro)?|mar(?:ço)?|abr(?:il)?|mai(?:o)?|jun(?:ho)?|jul(?:ho)?|ago(?:sto)?|set(?:embro)?|out(?:ubro)?|nov(?:embro)?|dez(?:embro)?))(?:\/|\.|\-)(?:\d{1,4}|(?:(?i)jan(?:eiro)?|fev(?:ereiro)?|mar(?:ço)?|abr(?:il)?|mai(?:o)?|jun(?:ho)?|jul(?:ho)?|ago(?:sto)?|set(?:embro)?|out(?:ubro)?|nov(?:embro)?|dez(?:embro)?))(?:(?:\/|\.|\-)[\d]+)?(?=\ |$|\.)
    |
    (?:[\w]+\$) # R$ e U$
    |
    (?:(?:\d+[,/.:-])*\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:(?i)ex-[\w]+) # ex-dividendos, etc.
    |
    (?:[$]?[^\W_](?:[^\W_]|['\_])+[^\W_]) # Words with apostrophes, considering numbers
    |
    (?:[\w\d]+\/[\w\d]?) # p/ e c/
    |
    (?:%k|&lt) # %k and &lt
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """,
)

######################################################################
# This is the core tokenizing regex:

WORD_RE = regex.compile(r"""(%s)""" % "|".join(REGEXPS), regex.VERBOSE | regex.I | regex.UNICODE)

# WORD_RE performs poorly on these patterns:
HANG_RE = regex.compile(r"([^a-zA-Z0-9])\1{3,}")

# The emoticon string gets its own regex so that we can preserve case for
# them as needed:
EMOTICON_RE = regex.compile(EMOTICONS, regex.VERBOSE | regex.I | regex.UNICODE)

# These are for regularizing HTML entities to Unicode:
ENT_RE = regex.compile(r"&(#?(x?))([^&;\s]+);")

#endregion

#region Functions for converting html entities


class DanteTokenizer:
    r"""
    Tokenizer for stock-market tweets.

        >>> from nltk.tokenize import DanteTokenizer
        >>> tknzr = DanteTokenizer()
        >>> s0 = "This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"
        >>> tknzr.tokenize(s0)
        ['This', 'is', 'a', 'cooool', '#dummysmiley', ':', ':-)', ':-P', '<3', 'and', 'some', 'arrows', '<', '>', '->', '<--']

    Examples using `strip_handles` and `reduce_len parameters`:

        >>> tknzr = DanteTokenizer(strip_handles=True, reduce_len=True)
        >>> s1 = '@remy: This is waaaaayyyy too much for you!!!!!!'
        >>> tknzr.tokenize(s1)
        [':', 'This', 'is', 'waaayyy', 'too', 'much', 'for', 'you', '!', '!', '!']
    """

    def __init__(self, preserve_case=True, reduce_len=False, strip_handles=False):
        self.preserve_case = preserve_case
        self.reduce_len = reduce_len
        self.strip_handles = strip_handles

    def tokenize(self, text):
        """
        :param text: str
        :rtype: list(str)
        :return: a tokenized list of strings; concatenating this list returns\
        the original string if `preserve_case=False`
        """
        # Fix HTML character entities:
        text = _replace_html_entities(text)
        # Normalize unicode text
        text = normalize_text(text)
        # Expanding contractions
        text = expand_contractions(text)
        # Splitting monetary tokens
        text = split_monetary_tokens(text)
        # Remove username handles
        if self.strip_handles:
            text = remove_handles(text)
        # Normalize word lengthening
        if self.reduce_len:
            text = reduce_lengthening(text)
        # Shorten problematic sequences of characters
        safe_text = HANG_RE.sub(r"\1\1\1", text)
        # Tokenize:
        words = WORD_RE.findall(safe_text)
        # Possibly alter the case, but avoid changing emoticons like :D into :d:
        if not self.preserve_case:
            words = list(
                map((lambda x: x if EMOTICON_RE.search(x) else x.lower()), words)
            )
        return words

def _str_to_unicode(text, encoding=None, errors="strict"):
    if encoding is None:
        encoding = "utf-8"
    if isinstance(text, bytes):
        return text.decode(encoding, errors)
    return text


def _replace_html_entities(text, keep=(), remove_illegal=True, encoding="utf-8"):
    """
    Remove entities from text by converting them to their
    corresponding unicode character.

    :param text: a unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    :param list keep:  list of entity names which should not be replaced.\
    This supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    :param bool remove_illegal: If `True`, entities that can't be converted are\
    removed. Otherwise, entities that can't be converted are kept "as
    is".

    :returns: A unicode string with the entities removed.

    See https://github.com/scrapy/w3lib/blob/master/w3lib/html.py

        >>> from nltk.tokenize.casual import _replace_html_entities
        >>> _replace_html_entities(b'Price: &pound;100')
        'Price: \\xa3100'
        >>> print(_replace_html_entities(b'Price: &pound;100'))
        Price: £100
        >>>
    """

    def _convert_entity(match):
        entity_body = match.group(3)
        if match.group(1):
            try:
                if match.group(2):
                    number = int(entity_body, 16)
                else:
                    number = int(entity_body, 10)
                # Numeric character references in the 80-9F range are typically
                # interpreted by browsers as representing the characters mapped
                # to bytes 80-9F in the Windows-1252 encoding. For more info
                # see: https://en.wikipedia.org/wiki/ISO/IEC_8859-1#Similar_character_sets
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
            except ValueError:
                number = None
        else:
            if entity_body in keep:
                return match.group(0)
            else:
                number = html.entities.name2codepoint.get(entity_body)
        if number is not None:
            try:
                return chr(number)
            except (ValueError, OverflowError):
                pass

        return "" if remove_illegal else match.group(0)

    return ENT_RE.sub(_convert_entity, _str_to_unicode(text, encoding))



#endregion

#region Normalization functions

def reduce_lengthening(text):
    """
    Replace repeated character sequences of length 3 or greater with sequences
    of length 3.
    """
    pattern = regex.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1\1", text)


def remove_handles(text):
    """
    Remove Twitter username handles from text.
    """
    pattern = regex.compile(
        r"(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)"
    )
    # Substitute handles with ' ' to ensure that text on either side of removed handles are tokenized correctly
    return pattern.sub(" ", text)

#endregion

def predict_nltk_word_tokenizer(sentences: list) -> list:
    """ 
    Predict all sentences sequentially.

    Parameters
    ----------
    sentences: list
        List of strings with pre-processed sentences.
    
    Retunrs
    -------
    list:
        List of predicted tokens for each sentenec.
    """
    pred_tokens = []

    for sentence in sentences:
        pred_tokens.append(tokenize.word_tokenize(sentence, language="portuguese"))

    return pred_tokens

def predict_nltk_twitter_tokenizer(sentences: list) -> list:
    """ 
    Predict all sentences sequentially.

    Parameters
    ----------
    sentences: list
        List of strings with pre-processed sentences.
    
    Retunrs
    -------
    list:
        List of predicted tokens for each sentenec.
    """
    pred_tokens = []

    tokenizer = tokenize.TweetTokenizer()

    for sentence in sentences:
        pred_tokens.append(tokenizer.tokenize(sentence))

    return pred_tokens

def predict_dante_tokenizer(sentences: list) -> list:
    """ 
    Predict all sentences sequentially.

    Parameters
    ----------
    sentences: list
        List of strings with pre-processed sentences.
    
    Retunrs
    -------
    list:
        List of predicted tokens for each sentenec.
    """
    pred_tokens = []

    tokenizer = DanteTokenizer()

    for sentence in sentences:
        pred_tokens.append(tokenizer.tokenize(sentence))

    return pred_tokens
