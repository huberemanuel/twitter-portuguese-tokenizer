constractions = {
    "no": "em o",
    "na": "em a"
}

def expand_contractions(text: str):

    for contraction in constractions.keys():
        if contraction in text:
            text = text.replace(contraction, constractions[contraction], 1)

    return text