import pytest

from dante_tokenizer import DanteTokenizer


@pytest.mark.parametrize(("raw_str", "expected_str"), [
    ("R$32,10", "R$ 32,10"),
    ("BMF&Bovespa", "BMF&Bovespa"),
    ("OIBR4", "OIBR4"),
    ("oibr4", "oibr4"),
    ("p/", "p/"),
    (":)", ":)"),
    (":(", ":("),
    ("=)", "=)"),
    ("=(", "=("),
    ("*.*", "*.*"),
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
])
def test_tokenizer(raw_str: str, expected_str: str):
    dt = DanteTokenizer()
    tokenized = dt.tokenize(raw_str)

    assert " ".join(tokenized) == expected_str

