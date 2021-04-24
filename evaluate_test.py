from evaluate import evaluate_sentence


def test_evaluate_sentence():
    """ Tests evaluate_sentence function on documented cases for DANTE dataset """

    # Case 1: Stock names
    assert evaluate_sentence(["Comprei", "PETR4", ","], ["Comprei", "PETR4", ","]) == (3, 0, 0)
    assert evaluate_sentence(["Comprei", "PETR", "4", ","], ["Comprei", "PETR4", ","]) == (2, 2, 1)

    # Case 2: "para" and "com" abbreviation
    assert evaluate_sentence(["Estou", "c/", "MGLU3"],
                             ["Estou", "c/", "MGLU3"]) == (3, 0, 0)
    assert evaluate_sentence(["Estou", "c", "/", "MGLU3"],
                             ["Estou", "c/", "MGLU3"]) == (2, 2, 1)
    assert evaluate_sentence(["Estou", "p/", "MGLU3"],
                             ["Estou", "p/", "MGLU3"]) == (3, 0, 0)
    assert evaluate_sentence(["Estou", "p", "/", "MGLU3"],
                             ["Estou", "p/", "MGLU3"]) == (2, 2, 1)

    # Case 3: Cash symbol
    assert evaluate_sentence(["Tenho", "R$", "1.000,00"],
                             ["Tenho", "R$", "1.000,00"]) == (3, 0, 0)
    assert evaluate_sentence(["Tenho", "R", "$", "1.000,00"],
                             ["Tenho", "R$", "1.000,00"]) == (2, 2, 1)
    assert evaluate_sentence(["Tenho", "U$", "1.000,00"],
                             ["Tenho", "U$", "1.000,00"]) == (3, 0, 0)
    assert evaluate_sentence(["Tenho", "U", "$", "1.000,00"],
                             ["Tenho", "U$", "1.000,00"]) == (2, 2, 1)

    # Case 4: Emotions and Emojis
    assert evaluate_sentence(["Oi", ":)"], ["Oi", ":)"]) == (2, 0, 0)
    assert evaluate_sentence(["Oi", ":", ")"], ["Oi", ":)"]) == (1, 2, 1)
    assert evaluate_sentence(["Oi", ":("], ["Oi", ":("]) == (2, 0, 0)
    assert evaluate_sentence(["Oi", ":", "("], ["Oi", ":("]) == (1, 2, 1)
    assert evaluate_sentence(["Oi", "=)"], ["Oi", "=)"]) == (2, 0, 0)
    assert evaluate_sentence(["Oi", "=", ")"], ["Oi", "=)"]) == (1, 2, 1)
    assert evaluate_sentence(["Oi", "=("], ["Oi", "=("]) == (2, 0, 0)
    assert evaluate_sentence(["Oi", "=", "("], ["Oi", "=("]) == (1, 2, 1)

    # Case 5: Data formats
    assert evaluate_sentence(["07/01/1997"], ["07/01/1997"]) == (1, 0, 0)
    assert evaluate_sentence(["07/01"], ["07/01"]) == (1, 0, 0)
    assert evaluate_sentence(["1997/01/07"], ["1997/01/07"]) == (1, 0, 0)
    assert evaluate_sentence(["07", "/", "01", "/", "1997"], ["07/01/1997"]) == (0, 5, 1)
    assert evaluate_sentence(["07", "/", "01"], ["07/01"]) == (0, 3, 1)
    assert evaluate_sentence(["1997", "/", "01", "/", "07"], ["1997/01/07"]) == (0, 5, 1)

    # Case 6: Mention and hashtags
    assert evaluate_sentence(["@elonmusk", "rocks"],
                             ["@elonmusk", "rocks"]) == (2, 0, 0)
    assert evaluate_sentence(["@", "elonmusk", "rocks"],
                             ["@elonmusk", "rocks"]) == (1, 2, 1)
    assert evaluate_sentence(["Lex", "Fridman", "#robot"],
                             ["Lex", "Fridman", "#robot"]) == (3, 0, 0)
    assert evaluate_sentence(["Lex", "Fridman", "#", "robot"],
                             ["Lex", "Fridman", "#robot"]) == (2, 2, 1)

    # Case 7: Stock market terminology
    assert evaluate_sentence(["$CTIP3", "rendeu"], ["$CTIP3", "rendeu"]) == (2, 0, 0)
    assert evaluate_sentence(["$", "CTIP3", "rendeu"], ["$CTIP3", "rendeu"]) == (1, 2, 1)
    assert evaluate_sentence(["alta", "no", "estocástico", "%k"],
                             ["alta", "no", "estocástico", "%k"]) == (4, 0, 0)
    assert evaluate_sentence(["alta", "no", "estocástico", "%", "k"],
                             ["alta", "no", "estocástico", "%k"]) == (3, 2, 1)
