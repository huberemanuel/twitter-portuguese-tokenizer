import argparse

from nltk import tokenize

from evaluate import read_test_data, evaluate_dataset


def nltk_word_tokenizer(sentences: list) -> list:
    pred_tokens = []

    for sentence in sentences:
        pred_tokens.append(tokenize.word_tokenize(sentence, language="portuguese"))

    return pred_tokens

def nltk_regex_tokenizer(sentences: list) -> list:
    pred_tokens = []

    tokenizer_regex = r'''(?ux)
    # the order of the patterns is important!!
    # more structured patterns come first
    [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+|    # emails
    (?:https?://)?\w{2,}(?:\.\w{2,})+(?:/\w+)*|                  # URLs
    (?:[\#@]\w+)|                     # Hashtags and twitter user names
    (?:[^\W\d_]\.)+|                  # one letter abbreviations, e.g. E.U.A.
    (?:[DSds][Rr][Aa]?)\.|            # common abbreviations such as dr., sr., sra., dra.
    (?:\B-)?\d+(?:[:.,]\d+)*(?:-?\w)*|
        # numbers in format 999.999.999,999, possibly followed by hyphen and alphanumerics
        # \B- avoids picks as F-14 as a negative number
    \.{3,}|                           # ellipsis or sequences of dots
    \w+|                              # alphanumerics
    -+|                               # any sequence of dashes
    \S                                # any non-space character
    '''

    tokenizer = tokenize.RegexpTokenizer(tokenizer_regex)

    for sentence in sentences:
        pred_tokens.append(tokenizer.tokenize(sentence))

    return pred_tokens

def main():

    ids, sentences, true_tokens = read_test_data("data/tweets_stocks.csv", "data/dante_tweets1a50.conllu")

    tokenizers = [
        ("nltk Word Tokenizer", nltk_word_tokenizer),
        ("nltk regex Tokenizer", nltk_regex_tokenizer)
    ]

    for name, tokenizer in tokenizers:
        pred_tokens = tokenizer(sentences)

        precision, recall = evaluate_dataset(pred_tokens, true_tokens)
        
        print(f"{name} precision: {precision*100:.2f}, recall: {recall*100:.2f}")

if __name__ == "__main__":
    main()