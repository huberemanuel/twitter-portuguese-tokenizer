import re

import pandas as pd

from dante_tokenizer.data.preprocessing import remove_quotes


def read_tokens_from_txt(txt_path: str, header: bool = False) -> (list, list):
    """
    Read txt file and return tokens. The txt file should contain a tokenized sentences
    for each line, were tokens are separated by spaces.

    txt_path: str
        Path to input txt_file
    header: bool
        Whetiher the file first line is a header or not.

    Returns
    -------
    (list, list):
        Sentence id (row number), list of tokens
    """
    with open(txt_path, "r") as txt_f:
        data = txt_f.readlines()
        if len(data) < 1 or len(data) < 2 and header:
            return []
        return list(range(len(data)))[1:], data[1:]


def read_tokens_from_csv(
    csv_path: str, start_line: int = 0, n_sentences: int = -1
) -> (list, list):
    """
    Read csv file and return tokens. The first colulmn should be
    the tweet_id and the second the sentence text.

    Parameters
    ----------
    csv_path: str
        Full path to the csv file.
    start_line: int
        Line number to start the reading
    n_sentences: int
        Number of sentences to retrieve sequentially from csv data.
        If n_sentences == -1, then it will return all lines.

    Returns
    -------
    (list, list):
        List of sentence ids and sentence texts.
    """
    sent_ids = []
    sent_texts = []

    # Unprocessable parameters
    if n_sentences < -1:
        raise ValueError("n_sentences must be a positive or equal to -1")
    elif start_line < 0:
        raise ValueError("start_line must be greater than 0")

    csv_df = pd.read_csv(csv_path)

    if n_sentences == -1:
        n_sentences = csv_df.shape[0]
    else:
        n_sentences = min(csv_df.shape[0], n_sentences + start_line)

    for index, row in csv_df.iloc[start_line:n_sentences, :].iterrows():

        sent_id = row["tweet_id"]
        sent_text = row["text"]
        sent_text = remove_quotes(sent_text)

        sent_ids.append(sent_id)
        sent_texts.append(sent_text)

    return sent_ids, sent_texts


def read_test_data(csv_path: str, conllu_path: str) -> dict:
    """
    Read the unparsed sentences from a csv formatted file, expecting the second
    column to contain the raw sentence. Secondily, reads the formatted dataset
    on the CoNNL-U format to extract sentence's tokens.

    Parameters
    ----------
    conllu_path: str
        Path to the conllu formatted dataset.

    Returns
    -------
    list
        List containing sentence ids.
    list
        List containing sentence original texts.
    list
        List containing a list of sentence tokens.
    """

    sent_ids = []
    sent_texts = []
    sent_tokens = []

    # TODO: Fix this regex, Won't work with last line from conllu file.
    conllu_sentence_regex = r"(# newdoc[\s\S]*?[\r\n]{2})"
    conllu_sentence_id_regex = r"sent_id = (dante_01_.*)"
    conllu_token_split_regex = r"^[\d]+\t([^\t]*)"

    csv_file = open(csv_path, "r")
    df = pd.read_csv(csv_path)
    conllu_file = open(conllu_path, "r")
    conllu_data = conllu_file.read()

    try:
        matches = re.finditer(conllu_sentence_regex, conllu_data)

        for matchNum, match in enumerate(matches, start=1):
            conllu_text = match.group(0)
            sent_id = re.findall(conllu_sentence_id_regex, conllu_text)[0]
            tokens = []

            tokens = re.findall(conllu_token_split_regex, conllu_text, re.MULTILINE)

            sentence = df[df["tweet_id"] == sent_id.split("_")[-1]]["text"].values[0]
            sentence = remove_quotes(sentence)

            sent_ids.append(sent_id)
            sent_texts.append(sentence)
            sent_tokens.append(tokens)

    finally:

        csv_file.close()
        conllu_file.close()

    return sent_ids, sent_texts, sent_tokens
