import pytest

from dante_tokenizer.data.preprocessing import expand_contractions


@pytest.mark.parametrize(("contracted", "expanded"), [
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
    ("à", "a a"),
    ("às", "a as"),
    ("pra", "para a"),
    ("pro", "para o"),
    ("pras", "para as"),
    ("pros", "para os"),
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
])
def tisest_contraction(contracted: str, expanded: str):
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

