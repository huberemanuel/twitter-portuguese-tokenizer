import argparse
import os

from dante_tokenizer.data.load import read_tokens_from_csv
from dante_tokenizer.data.preprocessing import reconstruct_html_chars, remove_quotes
from dante_tokenizer.tokenizer import DanteTokenizer


def tokenize_csv(csv_path: str, start_line: int, n_sentences: int) -> list:
    """
    Runs DanteTokenizer for each row in the csv file, it is expected
    to the first column be the sentence id and the second to be the
    sentence text.

    Parameters
    ----------
    csv_path: str
        Full path to the csv input file.

    Returns
    -------
    list
        List of parsed tokens for each sentence.
    """

    sent_ids, sent_texts = read_tokens_from_csv(csv_path, start_line, n_sentences)
    # Preprocess input
    sent_texts = list(map(remove_quotes, sent_texts))
    sent_texts = list(map(reconstruct_html_chars, sent_texts))
    tokenizer = DanteTokenizer()
    sent_tokens = list(map(tokenizer.tokenize, sent_texts))

    return sent_ids, sent_tokens, sent_texts


def tokens_to_conllu(
    doc_name: str, sent_ids: list, sent_tokens: list, sent_texts: list
) -> list:

    """
    Create conllu string representation based on original sentences and tokens.

    Parameters
    ----------
    doc_name: str
        Name of the given doc.
    sent_ids: list
        List of sentence ids.
    sent_tokens: list
        List of parsed tokens.
    sent_texts: list
        List of sentence texts.

    Returns:
        List of strings on the conllu format.
    """

    conllu_text = [""]

    for sent_id, sent_token, sent_text in zip(sent_ids, sent_tokens, sent_texts):
        conllu_text.append(f"# newdoc id = {doc_name}\n")
        conllu_text.append("# newpar\n")
        conllu_text.append(f"# sent_id = dante_01_{sent_id}\n")
        sent_text = sent_text.replace("\n", " ")
        conllu_text.append(f"# text = {sent_text}\n")

        for token_id, token in enumerate(sent_token, start=1):
            conllu_text.append(f"{token_id}\t{token}" + "\t_" * 7)
            if token_id == len(sent_token):
                conllu_text[-1] += "\tSpacesAfter=\\n\n"
            else:
                conllu_text[-1] += "\t_\n"
        conllu_text.append("\n")

    return conllu_text


def save_conllu(conllu_text: list, file_name: str) -> None:
    """
    Creates conllu file.

    Parameters
    ----------
    conllu_text: list
        List of strings on the conllu format
    file_name: str
        Output path to store the conllu file.
    """
    conllu_file = open(file_name, "w")

    for line in conllu_text:
        conllu_file.writelines(line)

    conllu_file.close()


def main():
    parser = argparse.ArgumentParser("Transforms csv file to conllu file")
    parser.add_argument("csv_path", type=str, help="Full path to the csv file")
    parser.add_argument(
        "--start_line",
        type=int,
        default=1,
        help="Start reading csv from specified line",
    )
    parser.add_argument(
        "--n_sentences", type=int, default=-1, help="Read n_sentences from csv data"
    )
    args = parser.parse_args()
    doc_name = os.path.basename(args.csv_path)
    sent_ids, sent_tokens, sent_texts = tokenize_csv(
        args.csv_path, args.start_line, args.n_sentences
    )
    conllu_text = tokens_to_conllu(doc_name, sent_ids, sent_tokens, sent_texts)
    save_conllu(conllu_text, f"{doc_name}.conllu")


if __name__ == "__main__":
    main()
