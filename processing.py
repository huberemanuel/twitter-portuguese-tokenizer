import re

constractions = {
    r"(?<![\w])no(?![$\w])": "em o",
    r"(?<![\w])na(?![$\w])": "em a",
    r"(?<![\w])da(?![$\w])": "de a",
    r"(?<![\w])do(?![$\w])": "de o",
    r"(?<![\w])das(?![$\w])": "de as",
    r"(?<![\w])dos(?![$\w])": "de os",
    r"(?<![\w])à(?![$\w])": "a a",
    r"(?<![\w])pra(?![$\w])": "para",
    r"(?<![\w])pro(?![$\w])": "para o"
}

def expand_contractions(text: str):
    # TODO: Aceitar letras maiúsculas também.
    for contraction in constractions.keys():
        text = re.sub(contraction, constractions[contraction], text)

    return text

def remove_quotes(text: str) -> str:
    quote_marks = ["\"", "“"]
    if text[0] in quote_marks and text[-1] in quote_marks:
        return text[1:-1]
    return text