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
])
def test_tokenizer(raw_str: str, expected_str: str):
    dt = DanteTokenizer()
    tokenized = dt.tokenize(raw_str)

    assert " ".join(tokenized) == expected_str
