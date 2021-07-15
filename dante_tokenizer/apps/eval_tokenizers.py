import argparse
import glob
import os

import latextable
from tabulate import tabulate
from texttable import Texttable

from dante_tokenizer.data.load import read_test_data
from dante_tokenizer.data.preprocessing import reconstruct_html_chars, remove_quotes
from dante_tokenizer.evaluate import evaluate_dataset
from dante_tokenizer.tokenizer import (
    predict_dante_tokenizer,
    predict_nltk_twitter_tokenizer,
    predict_nltk_word_tokenizer,
    predict_spacy,
    predict_twikenizer,
)


def main():

    parser = argparse.ArgumentParser(
        "Evaluate different tokenizers on Dante Dataset (Brazilian Stock-Market Tweets)"
    )
    parser.add_argument("csv_path", type=str, help="Path to the Dante dataset csv file")
    parser.add_argument(
        "conllu_path",
        type=str,
        help="Path to the conllu file containing tokenized sentences",
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Print detailed metrics and wrong sentence tokens",
    )
    parser.add_argument(
        "--output_table",
        default=False,
        action="store_true",
        help="Wheter to output latex code to put in your awesome paper or not.",
    )
    args = parser.parse_args()

    if os.path.isdir(args.conllu_path):
        ids, sentences, true_tokens = [], [], []
        for file_name in glob.glob(f"{args.conllu_path}/*.conllu"):
            _ids, _sentences, _true_tokens = read_test_data(args.csv_path, file_name)
            ids += _ids
            sentences += _sentences
            true_tokens += _true_tokens
    else:
        ids, sentences, true_tokens = read_test_data(args.csv_path, args.conllu_path)

    # Preprocess input
    sentences = list(map(remove_quotes, sentences))
    sentences = list(map(reconstruct_html_chars, sentences))

    tokenizers = [
        ("nltk Word Tokenizer", predict_nltk_word_tokenizer),
        ("nltk Twitter Tokenizer", predict_nltk_twitter_tokenizer),
        ("Twikenizer", predict_twikenizer),
        ("Spacy", predict_spacy),
        ("DANTE Tokenizer", predict_dante_tokenizer),
    ]

    table = [["Tokenizer", "Precision", "Recall", "Micro F-score"]]

    for name, tokenizer in tokenizers:
        pred_tokens = tokenizer(sentences)

        if not pred_tokens:
            continue

        precision, recall, f_score, extra_metrics = evaluate_dataset(
            pred_tokens, true_tokens, complete_metrics=True
        )

        table.append(
            [
                name,
                "{:.4f} ± {:.4f}".format(precision[0], precision[1]),
                "{:.4f} ± {:.4f}".format(recall[0], recall[1]),
                "{:.4f} ± {:.4f}".format(f_score[0], f_score[1]),
            ]
        )

        if args.debug:
            print(
                (
                    f"{name} precision: {precision}, recall: {recall}, "
                    + f"f_score: {f_score} "
                    + f"true_positives: {extra_metrics['true_positives']} "
                    + f"false_positives: {extra_metrics['false_positives']} "
                    + f"false_negatives: {extra_metrics['false_negatives']} "
                )
            )

        if args.debug:
            for incorrect_sentences_id in extra_metrics["incorrect_sentences_ids"]:
                print("*" * 20)
                print(pred_tokens[incorrect_sentences_id])
                print(true_tokens[incorrect_sentences_id])
            print()

    latex_table = Texttable()
    latex_table.set_cols_align(["c"] * 4)
    latex_table.set_deco(Texttable.HEADER | Texttable.VLINES)
    latex_table.add_rows(table)

    print(latex_table.draw())

    if args.output_table:
        print(tabulate(table, headers="firstrow", tablefmt="latex"))


if __name__ == "__main__":
    main()
