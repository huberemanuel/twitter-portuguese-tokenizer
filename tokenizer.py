import argparse

from nltk import tokenize

from evaluate import read_test_data, evaluate_dataset


def nltk_word_tokenizer(sentences: list) -> list:
    pred_tokens = []

    for sentence in sentences:
        pred_tokens.append(tokenize.word_tokenize(sentence, language="portuguese"))

    return pred_tokens

def main():

    ids, sentences, true_tokens = read_test_data("data/tweets_stocks.csv", "data/dante_tweets1a50.conllu")
    pred_tokens = nltk_word_tokenizer(sentences)

    precision, recall = evaluate_dataset(pred_tokens, true_tokens)
    
    print(f"NLTK word tokenizer precision: {precision*100:.2f}, recall: {recall*100:.2f}")

if __name__ == "__main__":
    main()