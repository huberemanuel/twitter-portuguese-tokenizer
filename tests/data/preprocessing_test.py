import pytest

from dante_tokenizer.data.preprocessing import (
    expand_contractions,
    split_enclisis,
    split_monetary_tokens,
)


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("perguntou-me", "perguntou - me"),
        ("perguntou-lhe", "perguntou - lhe"),
        ("perguntou-se", "perguntou - se"),
        ("perguntou-te", "perguntou - te"),
        ("perguntou-o", "perguntou - o"),
        ("perguntou-a", "perguntou - a"),
        ("perguntou-nos", "perguntou - nos"),
        ("perguntou-vos", "perguntou - vos"),
        ("perguntou-lhes", "perguntou - lhes"),
        ("perguntou-os", "perguntou - os"),
        ("perguntou-as", "perguntou - as"),
        ("perguntou-lo", "perguntou - lo"),
        ("perguntou-la", "perguntou - la"),
        ("perguntou-los", "perguntou - los"),
        ("perguntou-las", "perguntou - las"),
    ],
)
def test_split_enclisis(original: str, expected: str):
    assert split_enclisis(original) == expected


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("Sr. K tem 10milhões", "Sr. K tem 10 milhões"),
        ("Sr. K tem 10mi", "Sr. K tem 10 mi"),
        ("Sr. K tem 10M", "Sr. K tem 10 M"),
        ("Sr. K tem 10m", "Sr. K tem 10 m"),
        ("Sr. K tem 10bilhões", "Sr. K tem 10 bilhões"),
        ("Sr. K tem 10bi", "Sr. K tem 10 bi"),
        ("Sr. K tem 10B", "Sr. K tem 10 B"),
        ("Sr. K tem 10b", "Sr. K tem 10 b"),
    ],
)
def test_split_monetary_tokens(original: str, expected: str):
    assert split_monetary_tokens(original) == expected


@pytest.mark.parametrize(
    ("contracted", "expanded"),
    [
        ("no", "em o"),
        ("na", "em a"),
        ("nos", "em os"),
        ("nas", "em as"),
        ("do", "de o"),
        ("da", "de a"),
        ("dos", "de os"),
        ("das", "de as"),
        ("ao", "a o"),
        ("aos", "a os"),
        ("às", "a as"),
        ("pela", "por a"),
        ("pelo", "por o"),
        ("pelas", "por as"),
        ("pelos", "por os"),
        ("nesta", "em esta"),
        ("neste", "em este"),
        ("nestas", "em estas"),
        ("nestes", "em estes"),
        ("nessa", "em essa"),
        ("nesse", "em esse"),
        ("nessas", "em essas"),
        ("nesses", "em esses"),
        ("num", "em um"),
        ("numa", "em uma"),
        ("nuns", "em uns"),
        ("numas", "em umas"),
        ("daqui", "de aqui"),
        ("desta", "de esta"),
        ("deste", "de este"),
        ("destas", "de estas"),
        ("destes", "de estes"),
        ("daí", "de aí"),
        ("donde", "de onde"),
        ("daquele", "de aquele"),
        ("daquela", "de aquela"),
        ("daqueles", "de aqueles"),
        ("daquelas", "de aquelas"),
        ("disto", "de isto"),
        ("disso", "de isso"),
        ("desse", "de esse"),
        ("daquilo", "de aquilo"),
        ("dela", "de ela"),
        ("dele", "de ele"),
        ("delas", "de elas"),
        ("deles", "de eles"),
        ("nisto", "em isto"),
        ("nele", "em ele"),
        ("nela", "em ela"),
        ("neles", "em eles"),
        ("nelas", "em elas"),
        ("aonde", "a onde"),
        ("Estou testando aonde", "Estou testando a onde"),
        ("contigo estou", "com ti estou"),
        ("né", "não é"),
    ],
)
def test_contraction(contracted: str, expanded: str):
    for i in range(3):
        for cap in [True, False]:
            input_str = contracted
            expected_str = expanded
            if cap:
                input_str = input_str.capitalize()
                expected_str = expected_str.capitalize()
            if i > 0:
                input_str += f" {input_str}" * i
                expected_str += f" {expected_str}" * i
            assert expand_contractions(input_str) == expected_str

            if not cap:
                input_str = input_str.upper()
                expected_str = expected_str.upper()
                assert expand_contractions(input_str) == expected_str
