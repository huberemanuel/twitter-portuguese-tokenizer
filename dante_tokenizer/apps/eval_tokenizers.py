import os
import glob
import argparse

from dante_tokenizer.data.load import read_test_data
from dante_tokenizer.data.preprocessing import remove_quotes
from dante_tokenizer.evaluate import evaluate_dataset
from dante_tokenizer.tokenizer import (
    predict_dante_tokenizer, 
    predict_nltk_twitter_tokenizer, 
    predict_nltk_word_tokenizer
)


def main():

    parser = argparse.ArgumentParser("Evaluate different tokenizers on Dante Dataset (Brazilian Stock-Market Tweets)")
    parser.add_argument("csv_path", type=str, help="Path to the Dante dataset csv file")
    parser.add_argument("conllu_path", type=str, help="Path to the conllu file containing tokenized sentences")
    parser.add_argument("--debug", default=False, action="store_true", 
                        help="Print detailed metrics and wrong sentence tokens")
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
    
    tokenizers = [
        ("nltk Word Tokenizer", predict_nltk_word_tokenizer),
        ("nltk Twitter Tokenizer", predict_nltk_twitter_tokenizer),
        ("DANTE Tokenizer", predict_dante_tokenizer)
    ]

    for name, tokenizer in tokenizers:
        pred_tokens = tokenizer(sentences)

        precision, recall, f_score, extra_metrics = evaluate_dataset(pred_tokens, true_tokens, complete_metrics=True)
        
        print((f"{name} precision: {precision}, recall: {recall}, f_score: {f_score} true_positives: {extra_metrics['true_positives']} "
               f"false_positives: {extra_metrics['false_positives']} false_negatives: {extra_metrics['false_negatives']} "))

        if args.debug:
            for incorrect_sentences_id in extra_metrics["incorrect_sentences_ids"]:
                print("*"*20)
                print(pred_tokens[incorrect_sentences_id])
                print(true_tokens[incorrect_sentences_id])
            print()

if __name__ == "__main__":
    main()

