import pytest

from dante_tokenizer import DanteTokenizer


@pytest.mark.parametrize(("raw_str", "expected_str"), [
    ("R$32,10", "R$ 32,10"),
    ("R$4.750,22", "R$ 4.750,22"),
    ("R$ 4.750,22", "R$ 4.750,22"),
    ("123123123123123,123123123123", "123123123123123,123123123123"),
    ("BMF&Bovespa", "BMF&Bovespa"),
    ("OIBR4", "OIBR4"),
    ("oibr4", "oibr4"),
    ("p/", "p/"),
    (":)", ":)"),
    (":)))", ":)))"),
    (":(((", ":((("),
    ("=)))", "=)))"),
    ("=(((", "=((("),
    ("*.*", "*.*"),
    ("***.***", "***.***"),
    ("02/03/2020", "02/03/2020"),
    ("20/21", "20/21"),
    ("02.03.2020", "02.03.2020"),
    ("20.21", "20.21"),
    ("02-03-2020", "02-03-2020"),
    ("20-21", "20-21"),
    ("@user123", "@user123"),
    ("#hashtag", "#hashtag"),
    ("%k", "%k"),
    ("1mil", "1 mil"),
    ("1milhão", "1 milhão"),
    ("1bilhão", "1 bilhão"),
    ("1trilhão", "1 trilhão"),
    ("1bi", "1 bi"),
    ("1tri", "1 tri"),
    ("p/a", "p/a"),
    ("P/a", "P/a"),
    ("ex-teste", "ex-teste"),
    ("ex-LLX", "ex-LLX"),
    ("ex-dividendos", "ex-dividendos"),
])
def test_tokenizer(raw_str: str, expected_str: str):
    dt = DanteTokenizer()
    raw = raw_str
    expected = expected_str

    for upper_case in [False, True]:
        for add_space in [False, 0, -1]:
            if add_space:
                if add_space == 0:
                    raw = " " + raw_str
                elif add_space == -1:
                    raw = raw_str + " "
            if upper_case:
                raw = raw.upper()
                expected = expected.upper()
            tokenized = dt.tokenize(raw)

            assert " ".join(tokenized) == expected

