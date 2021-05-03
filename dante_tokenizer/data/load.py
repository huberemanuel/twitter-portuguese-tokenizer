import re

from dante_tokenizer.data.preprocessing import expand_contractions, remove_quotes, split_monetary_tokens

def read_tokens_from_csv(csv_path: str) -> list:
    """
    """
    sent_ids = []
    sent_texts = []

    csv_split_regex = r"(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))"

    csv_file = open(csv_path, "r")
    csv_data = csv_file.readlines()

    for csv_line in csv_data[1:]:

        tokens_matches = re.findall(csv_split_regex, csv_line)

        sent_id = tokens_matches[0]
        sent_text = tokens_matches[1]
        sent_text = remove_quotes(sent_text)
        sent_text = expand_contractions(sent_text)
        sent_texts = split_monetary_tokens(text)

        sent_ids.append(sent_id)
        sent_texts.append(sent_text)

    csv_file.close()

    return sent_ids, sent_texts

def read_test_data(csv_path: str, conllu_path: str) -> dict:
    """
    Read the unparsed sentences from a csv formatted file, expecting the second 
    column to contain the raw sentence. Secondily, reads the formatted dataset 
    on the CoNNL-U format to extract sentence's tokens.

    Obs: This function assumes that the row number of the csv_path file corresponds
    to the conllu_path file `sent_id` field.

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
    conllu_sentence_id_regex = r"sent_id = ([\d]+)"
    conllu_token_split_regex = r"\d\t([^\t]*)"
    csv_split_regex = r"(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))"

    csv_file = open(csv_path, "r")
    csv_data = csv_file.readlines()
    conllu_file = open(conllu_path, "r")
    conllu_data = conllu_file.read()

    try:
        matches = re.finditer(conllu_sentence_regex, conllu_data)

        for matchNum, match in enumerate(matches, start=1):
            conllu_text = match.group(0)
            id_matches = re.finditer(conllu_sentence_id_regex, conllu_text)
            for id_match in id_matches:
                sent_id = int(id_match.group(1)) 
            tokens = []
            
            token_matches = re.finditer(conllu_token_split_regex, conllu_text)
            for token_match in token_matches:
                tokens.append(token_match.group(1))

            csv_line = csv_data[sent_id]
            csv_matches = re.findall(csv_split_regex, csv_line)
            sentence = csv_matches[1]
            # Pre-processing text
            sentence = remove_quotes(sentence)
            sentence = expand_contractions(sentence)
            sentence = split_monetary_tokens(sentence)

            sent_ids.append(sent_id)
            sent_texts.append(sentence)
            sent_tokens.append(tokens)

    finally:

        csv_file.close()
        conllu_file.close()

    return sent_ids, sent_texts, sent_tokens