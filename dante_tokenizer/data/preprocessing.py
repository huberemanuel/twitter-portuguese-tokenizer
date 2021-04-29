import re

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
    r"(?<![\w.])pra(?![$\w])": "para",
    r"(?<![\w.])pro(?![$\w])": "para o",
    r"(?<![\w.])pela(?![$\w])": "por a",
    r"(?<![\w.])pelo(?![$\w])": "por o",
    r"(?<![\w.])pelas(?![$\w])": "por as",
    r"(?<![\w.])pelos(?![$\w])": "por os",
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
    r"(?<![\w.])À(?![$\w])": "A A",
    r"(?<![\w.])Às(?![$\w])": "A As",
    r"(?<![\w.])Pra(?![$\w])": "Para",
    r"(?<![\w.])Pro(?![$\w])": "Para o",
    r"(?<![\w.])Pela(?![$\w])": "Por a",
    r"(?<![\w.])Pelo(?![$\w])": "Por o",
    r"(?<![\w.])Pelas(?![$\w])": "Por as",
    r"(?<![\w.])Pelos(?![$\w])": "Por os",
}

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

    text = text.replace("\'\'", "\"")

    quote_marks = ["\"", "“", "”"]
    if text[0] in quote_marks and text[-1] in quote_marks:
        text = text[1:-1]

    for quote_mark in ["\"", "\'"]:
        if text.count(quote_mark) % 2 != 0:
            text = text.replace(quote_mark, "", 1)
    return text