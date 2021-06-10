import re
import unicodedata


# TODO: Consider Caps Lock cases.
contractions = {
    r"(?<![\w.])no(s)?(?![$\w])": r"em o\g<1>",
    r"(?<![\w.])na(s)?(?![$\w])": r"em a\g<1>",
    r"(?<![\w.])da(s)?(?![$\w])": r"de a\g<1>",
    r"(?<![\w.])do(s)?(?![$\w])": r"de o\g<1>",
    r"(?<![\w.])ao(s)?(?![$\w])": r"a o\g<1>",
    r"(?<![\w.])à(s)?(?![$\w])": r"a a\g<1>",
    r"(?<![\w.])pela(s)?(?![$\w])": r"por a\g<1>",
    r"(?<![\w.])pelo(s)?(?![$\w])": r"por o\g<1>",
    r"(?<![\w.])nesta(s)?(?![$\w])": r"em esta\g<1>",
    r"(?<![\w.])neste(s)?(?![$\w])": r"em este\g<1>",
    r"(?<![\w.])nessa(s)?(?![$\w])": r"em essa\g<1>",
    r"(?<![\w.])nesse(s)?(?![$\w])": r"em esse\g<1>",
    r"(?<![\w.])num(?![$\w])": r"em um",
    r"(?<![\w.])nuns(?![$\w])": r"em uns",
    r"(?<![\w.])numa(s)?(?![$\w])": r"em uma\g<1>",
    r"(?<![\w.])daqui(?![$\w])": r"de aqui",
    r"(?<![\w.])daquele(s)?(?![$\w])": r"de aquele\g<1>",
    r"(?<![\w.])daquela(s)?(?![$\w])": r"de aquela\g<1>",
    r"(?<![\w.])deste(s)?(?![$\w])": r"de este\g<1>",
    r"(?<![\w.])desta(s)?(?![$\w])": r"de esta\g<1>",
    r"(?<![\w.])desse(s)?(?![$\w])": r"de esse\g<1>",
    r"(?<![\w.])dessa(s)?(?![$\w])": r"de essa\g<1>",
    r"(?<![\w.])daí(?![$\w])": r"de aí",
    r"(?<![\w.])donde(?![$\w])": r"de onde",
    r"(?<![\w.])disto(?![$\w])": r"de isto",
    r"(?<![\w.])disso(?![$\w])": r"de isso",
    r"(?<![\w.])daquilo(?![$\w])": r"de aquilo",
    r"(?<![\w.])dela(s)?(?![$\w])": r"de ela\g<1>",
    r"(?<![\w.])dele(s)?(?![$\w])": r"de ele\g<1>",
    r"(?<![\w.])nisto(?![$\w])": r"em isto",
    r"(?<![\w.])nele(s)?(?![$\w])": r"em ele\g<1>",
    r"(?<![\w.])nela(s)?(?![$\w])": r"em ela\g<1>",
    r"(?<![\w.])aonde(?![$\w])": r"a onde",
    r"(?<![\w.])contigo(?![$\w])": r"com ti",
    r"(?<![\w.])né(?![$\w])": r"não é",
}
enclisis = ['me', 'te', 'se', 'lhe', 'o', 'a', 'nos', 'vos', 'lhes', 'os', 'as', 'lo', 'la', 'los', 'las']


def split_enclisis(text: str):
    for enc in enclisis:
        text = re.sub(r"\b(\w+)-("+enc+r")\b", r"\g<1> - \g<2>", text, flags=re.I)
    return text

def reconstruct_html_chars(text: str) -> str:
    """
    Reconstrcut html chars from &gt, to &gt;

    Paramters
    ---------
    text: str
        Input text.

    Returns
    -------
    str:
        Processed str.
    """

    wrong_char_regex = r"(\&[\w\d]+),"
    
    if not "&" in text:
        return text

    text = re.sub(wrong_char_regex, r"\1;", text)

    return text

def split_monetary_tokens(text: str) -> str:
    """
    Split monetary text and numbers.
    Ex: Sr. K tem 10milhões -> Sr. K tem 10 milhões

    Parameters
    ----------
    text: str
        Input sentence.
    
    Returns
    -------
    str:
        Processed sentence.
    """
    text = re.sub(r"\b(\d+)((?i)(?:mi?|tri?|bi?)(?:ilh)?[õoaã]?[oe]?s?|mil)\b", r"\g<1> \g<2>",text)
    return text

def replace_keep_case(word, replacement, text):
    """
    Custom function for replace keeping the original case.

    Parameters
    ----------
    word: str
        Text to be replaced.
    replacement: str
        String to replace word.
    text:
        Text to be processed.

    Returns
    -------
    str:
        Processed string
    """
    def func(match):
        g = match.group()
        repl = match.expand(replacement)
        if g.islower(): return repl.lower()
        if g.istitle(): return repl.capitalize()
        if g.isupper(): return repl.upper()
        return repl

    return re.sub(word, func, text, flags=re.I)

def expand_contractions(text: str) -> str:
    """
    Replace contractions to their based form.

    Parameters
    ----------
    text: str
        Text that may contain contractions.
    
    Returns
    -------
    str:
        Text with expanded contractions.
    """

    for contraction in contractions.keys():
        replace_str = contractions[contraction]
        text = replace_keep_case(contraction, replace_str, text)

    return text

def normalize_text(text:str) -> str:
    """
    Normalize text to NFC which represents chars as an unique code.

    Parameters
    ----------
    text: str
        Input text string.

    Returns
    -------
    str:
        Normalized text.
    """
    return unicodedata.normalize("NFC", text)

def remove_quotes(text: str) -> str:
    """
    Replace '' to double quotes.
    Remove quotes in the beginning and end of a sentence.
    Remove beginning quotes without end quotes.

    Parameters
    ----------
    text:str
        Input sentence.
    
    Returns
    -------
    str:
        Cleaned text.
    """

    if len(text) < 3:
        return text

    text = text.replace("\'\'", "\"")

    quote_marks = ["\"", "“", "”"]
    if text[0] in quote_marks and text[-1] in quote_marks:
        text = text[1:-1]

    for quote_mark in ["\"", "\'"]:
        if text.count(quote_mark) % 2 != 0:
            text = text.replace(quote_mark, "", 1)
    return text

