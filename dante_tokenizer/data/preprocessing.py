import re
import unicodedata


# TODO: Consider Caps Lock cases.
contractions = {
    r"(?<![\w.])no(s)?(?![$\w])": r"em o\1",
    r"(?<![\w.])na(s)?(?![$\w])": r"em a\1",
    r"(?<![\w.])da(s)?(?![$\w])": r"de a\1",
    r"(?<![\w.])do(s)?(?![$\w])": r"de o\1",
    r"(?<![\w.])ao(s)?(?![$\w])": r"a o\1",
    r"(?<![\w.])à(s)?(?![$\w])": r"a a\1",
    r"(?<![\w.])pra(s)?(?![$\w])": r"para a\1",
    r"(?<![\w.])pro(s)?(?![$\w])": r"para o\1",
    r"(?<![\w.])pela(s)?(?![$\w])": r"por a\1",
    r"(?<![\w.])pelo(s)?(?![$\w])": r"por o\1",
    r"(?<![\w.])nesta(s)?(?![$\w])": r"em esta\1",
    r"(?<![\w.])neste(s)?(?![$\w])": r"em este\1",
    r"(?<![\w.])nessa(s)?(?![$\w])": r"em essa\1",
    r"(?<![\w.])nesse(s)?(?![$\w])": r"em esse\1",
    r"(?<![\w.])num(?![$\w])": r"em um",
    r"(?<![\w.])nuns?(?![$\w])": r"em uns",
    r"(?<![\w.])numa(s)?(?![$\w])": r"em uma\1",
    r"(?<![\w.])daqui(?![$\w])": r"de aqui",
    r"(?<![\w.])daquele(s)?(?![$\w])": r"de aquele\1",
    r"(?<![\w.])daquela(s)?(?![$\w])": r"de aquela\1",
    r"(?<![\w.])deste(s)?(?![$\w])": r"de este\1",
    r"(?<![\w.])desta(s)?(?![$\w])": r"de esta\1",
    r"(?<![\w.])desse(s)?(?![$\w])": r"de esse\1",
    r"(?<![\w.])dessa(s)?(?![$\w])": r"de essa\1",
    r"(?<![\w.])daí(?![$\w])": r"de aí",
    r"(?<![\w.])donde(?![$\w])": r"de onde",
    r"(?<![\w.])disto(?![$\w])": r"de isto",
    r"(?<![\w.])disso(?![$\w])": r"de isso",
    r"(?<![\w.])desse(?![$\w])": r"de esse",
    r"(?<![\w.])daquilo(?![$\w])": r"de aquilo",
    r"(?<![\w.])dela(s)?(?![$\w])": r"de ela\1",
    r"(?<![\w.])dele(s)?(?![$\w])": r"de ele\1",
    r"(?<![\w.])nisto(?![$\w])": r"em isto",
    r"(?<![\w.])nele(s)?(?![$\w])": r"em ele\1",
    r"(?<![\w.])nela(s)?(?![$\w])": r"em ela\1",
}

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
    text = re.sub(r"(\d)((?i)(?:m|tr|b)(?:ilh)?[õoaã]?[oe]?s?|mil)", r"\g<1> \g<2>",text)
    return text

def expand_contractions(text: str) -> str:
    """
    Replace contractions to their based form.

    Parameters
    ----------
    text: str
        Text that may contain contractions.
    
    Retunrs
    -------
    str:
        Text with expanded contractions.
    """

    for contraction in contractions.keys():
        replace_str = contractions[contraction]
        if text.isupper():
            replace_str = replace_str.upper()
        elif sum([x.isupper() for x in text]) > 0:
            # Solves capitalized strings, but not cases such nO or nElAs
            replace_str = replace_str.capitalize()
        text = re.sub(contraction, replace_str, text, flags=re.IGNORECASE)

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

