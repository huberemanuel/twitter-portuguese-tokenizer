import argparse

from nltk import tokenize

from evaluate import read_test_data, evaluate_dataset
from causal import TweetTokenizer


def nltk_word_tokenizer(sentences: list) -> list:
    pred_tokens = []

    for sentence in sentences:
        pred_tokens.append(tokenize.word_tokenize(sentence, language="portuguese"))

    return pred_tokens

def nltk_twitter_tokenizer(sentences: list) -> list:
    pred_tokens = []

    tokenizer = TweetTokenizer()

    for sentence in sentences:
        pred_tokens.append(tokenizer.tokenize(sentence))

    return pred_tokens

def main():

    ids, sentences, true_tokens = read_test_data("data/tweets_stocks.csv", "data/dante_tweets1a50.conllu")
    debug = True
    tokenizers = [
        ("nltk Word Tokenizer", nltk_word_tokenizer),
        ("nltk Twitter Tokenizer", nltk_twitter_tokenizer)
    ]

    for name, tokenizer in tokenizers:
        pred_tokens = tokenizer(sentences)

        if debug:
            for pred, true in zip(pred_tokens, true_tokens):
                print(f"{pred}\t\n{true}")
                print("-"*20)

        precision, recall = evaluate_dataset(pred_tokens, true_tokens)
        
        print(f"{name} precision: {precision*100:.2f}, recall: {recall*100:.2f}")

if __name__ == "__main__":
    main()