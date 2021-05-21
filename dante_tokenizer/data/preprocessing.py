import re
import unicodedata


# TODO: Consider Caps Lock cases.
constractions = {
    r"(?<![\w.])no(?![$\w])": "em o",
    r"(?<![\w.])na(?![$\w])": "em a",
    r"(?<![\w.])nos(?![$\w])": "em os",
    r"(?<![\w.])nas(?![$\w])": "em as",
    r"(?<![\w.])da(?![$\w])": "de a",
    r"(?<![\w.])do(?![$\w])": "de o",
    r"(?<![\w.])das(?![$\w])": "de as",
    r"(?<![\w.])dos(?![$\w])": "de os",
    r"(?<![\w.])ao(?![$\w])": "a o",
    r"(?<![\w.])aos(?![$\w])": "a os",
    r"(?<![\w.])à(?![$\w])": "a a",
    r"(?<![\w.])às(?![$\w])": "a as",
    r"(?<![\w.])pra(?![$\w])": "para a",
    r"(?<![\w.])pro(?![$\w])": "para o",
    r"(?<![\w.])pras(?![$\w])": "para as",
    r"(?<![\w.])pros(?![$\w])": "para os",
    r"(?<![\w.])pela(?![$\w])": "por a",
    r"(?<![\w.])pelo(?![$\w])": "por o",
    r"(?<![\w.])pelas(?![$\w])": "por as",
    r"(?<![\w.])pelos(?![$\w])": "por os",
    r"(?<![\w.])nesta(?![$\w])": "em esta",
    r"(?<![\w.])neste(?![$\w])": "em este",
    r"(?<![\w.])nestas(?![$\w])": "em estas",
    r"(?<![\w.])nestes(?![$\w])": "em estes",
    r"(?<![\w.])nessa(?![$\w])": "em essa",
    r"(?<![\w.])nesse(?![$\w])": "em esse",
    r"(?<![\w.])nessas(?![$\w])": "em essas",
    r"(?<![\w.])nesses(?![$\w])": "em esses",
    r"(?<![\w.])num(?![$\w])": "em um",
    r"(?<![\w.])numa(?![$\w])": "em uma",
    r"(?<![\w.])nuns(?![$\w])": "em uns",
    r"(?<![\w.])numas(?![$\w])": "em umas",
    r"(?<![\w.])daqui(?![$\w])": "de aqui",
    r"(?<![\w.])daquele(?![$\w])": "de aquele",
    r"(?<![\w.])daquela(?![$\w])": "de aquela",
    r"(?<![\w.])daqueles(?![$\w])": "de aqueles",
    r"(?<![\w.])daquelas(?![$\w])": "de aquelas",
    r"(?<![\w.])deste(?![$\w])": "de este",
    r"(?<![\w.])desta(?![$\w])": "de esta",
    r"(?<![\w.])destes(?![$\w])": "de estes",
    r"(?<![\w.])destas(?![$\w])": "de estas",
    r"(?<![\w.])desse(?![$\w])": "de esse",
    r"(?<![\w.])dessa(?![$\w])": "de essa",
    r"(?<![\w.])desses(?![$\w])": "de esses",
    r"(?<![\w.])dessas(?![$\w])": "de essas",
    r"(?<![\w.])daí(?![$\w])": "de aí",
    r"(?<![\w.])donde(?![$\w])": "de onde",
    r"(?<![\w.])disto(?![$\w])": "de isto",
    r"(?<![\w.])disso(?![$\w])": "de isso",
    r"(?<![\w.])desse(?![$\w])": "de esse",
    r"(?<![\w.])daquilo(?![$\w])": "de aquilo",
    r"(?<![\w.])dela(?![$\w])": "de ela",
    r"(?<![\w.])dele(?![$\w])": "de ele",
    r"(?<![\w.])delas(?![$\w])": "de elas",
    r"(?<![\w.])deles(?![$\w])": "de eles",
    r"(?<![\w.])nisto(?![$\w])": "em isto",
    r"(?<![\w.])nele(?![$\w])": "em ele",
    r"(?<![\w.])nela(?![$\w])": "em ela",
    r"(?<![\w.])neles(?![$\w])": "em eles",
    r"(?<![\w.])nelas(?![$\w])": "em elas",
    r"(?<![\w.])No(?![$\w])": "Em o",
    r"(?<![\w.])Na(?![$\w])": "Em a",
    r"(?<![\w.])Nos(?![$\w])": "Em os",
    r"(?<![\w.])Nas(?![$\w])": "Em as",
    r"(?<![\w.])Da(?![$\w])": "De a",
    r"(?<![\w.])Do(?![$\w])": "De o",
    r"(?<![\w.])Das(?![$\w])": "De as",
    r"(?<![\w.])Dos(?![$\w])": "De os",
    r"(?<![\w.])Ao(?![$\w])": "A o",
    r"(?<![\w.])Aos(?![$\w])": "A os",
    r"(?<![\w.])À(?![$\w])": "A a",
    r"(?<![\w.])Às(?![$\w])": "A as",
    r"(?<![\w.])Pra(?![$\w])": "Para a",
    r"(?<![\w.])Pro(?![$\w])": "Para o",
    r"(?<![\w.])Pras(?![$\w])": "Para as",
    r"(?<![\w.])Pros(?![$\w])": "Para os",
    r"(?<![\w.])Pela(?![$\w])": "Por a",
    r"(?<![\w.])Pelo(?![$\w])": "Por o",
    r"(?<![\w.])Pelas(?![$\w])": "Por as",
    r"(?<![\w.])Pelos(?![$\w])": "Por os",
    r"(?<![\w.])Nesta(?![$\w])": "Em esta",
    r"(?<![\w.])Neste(?![$\w])": "Em este",
    r"(?<![\w.])Nestas(?![$\w])": "Em estas",
    r"(?<![\w.])Nestes(?![$\w])": "Em estes",
    r"(?<![\w.])Nessa(?![$\w])": "Em essa",
    r"(?<![\w.])Nesse(?![$\w])": "Em esse",
    r"(?<![\w.])Nessas(?![$\w])": "Em essas",
    r"(?<![\w.])Nesses(?![$\w])": "Em esses",
    r"(?<![\w.])Num(?![$\w])": "Em um",
    r"(?<![\w.])Numa(?![$\w])": "Em uma",
    r"(?<![\w.])Nuns(?![$\w])": "Em uns",
    r"(?<![\w.])Numas(?![$\w])": "Em umas",
    r"(?<![\w.])Daqui(?![$\w])": "De aqui",
    r"(?<![\w.])Deste(?![$\w])": "De este",
    r"(?<![\w.])Desta(?![$\w])": "De esta",
    r"(?<![\w.])Destes(?![$\w])": "De estes",
    r"(?<![\w.])Destas(?![$\w])": "De estas",
    r"(?<![\w.])Desse(?![$\w])": "De esse",
    r"(?<![\w.])Dessa(?![$\w])": "De essa",
    r"(?<![\w.])Desses(?![$\w])": "De esses",
    r"(?<![\w.])Dessas(?![$\w])": "De essas",
    r"(?<![\w.])Daí(?![$\w])": "De aí",
    r"(?<![\w.])Donde(?![$\w])": "De onde",
    r"(?<![\w.])Daquele(?![$\w])": "De aquele",
    r"(?<![\w.])Daquela(?![$\w])": "De aquela",
    r"(?<![\w.])Daqueles(?![$\w])": "De aqueles",
    r"(?<![\w.])Daquelas(?![$\w])": "De aquelas",
    r"(?<![\w.])Disto(?![$\w])": "De isto",
    r"(?<![\w.])Disso(?![$\w])": "De isso",
    r"(?<![\w.])Desse(?![$\w])": "De esse",
    r"(?<![\w.])Daquilo(?![$\w])": "De aquilo",
    r"(?<![\w.])Dela(?![$\w])": "De ela",
    r"(?<![\w.])Dele(?![$\w])": "De ele",
    r"(?<![\w.])Delas(?![$\w])": "De elas",
    r"(?<![\w.])Deles(?![$\w])": "De eles",
    r"(?<![\w.])Nisto(?![$\w])": "Em isto",
    r"(?<![\w.])Nele(?![$\w])": "Em ele",
    r"(?<![\w.])Nela(?![$\w])": "Em ela",
    r"(?<![\w.])Neles(?![$\w])": "Em eles",
    r"(?<![\w.])Nelas(?![$\w])": "Em elas",
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

    for contraction in constractions.keys():
        text = re.sub(contraction, constractions[contraction], text)

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

