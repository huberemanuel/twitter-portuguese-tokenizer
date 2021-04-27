import re


def longest_common_token_sequence(left: list, right: list) -> int:
    """
    Implementation of Longest Common Subsequence using lists of tokens
    instead of strings, hence Longest Common Token Sequence.

    Parameters
    ----------
    left: list
        First first of tokens
    right: list
        Second list of tokens
    i_left: int
        Index for iterating over left list
    i_right: int
        Index for iterating over right list

    Returns
    -------
    int
        Size of the Logest Common Token Sequence found.
    """

    n_left = len(left)
    n_right = len(right)

    L = [[None]*(n_right+1) for i in range(n_left+1)]

    for i in range(n_left+1):
        for j in range(n_right+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif left[i-1] == right[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j] , L[i][j-1])

    return L[n_left][n_right]

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
    csv_split_regex = r"(?:^|,)(?=[^\"“]|(\"“)?)[\"“]?((?(1)[^\"“]*|[^,\"“]*))[\"“]?(?=,|$)"

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
            sentence = csv_matches[1][1]

            sent_ids.append(sent_id)
            sent_texts.append(sentence)
            sent_tokens.append(tokens)

    finally:

        csv_file.close()
        conllu_file.close()

    return sent_ids, sent_texts, sent_tokens

def evaluate_dataset(pred_tokens: list, true_tokens: list) -> (float, float):
    
    assert len(pred_tokens) == len(true_tokens)
    n_tokens = len(pred_tokens)
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for i in range(n_tokens):
        tp, fp, fn = evaluate_sentence(pred_tokens[i], true_tokens[i])
        true_positives += tp
        false_positives += fp
        false_negatives += fn

    precision = tp / (tp + fp + 1e-9)
    recall = tp / (tp + fn + 1e-9)

    return precision, recall

def evaluate_sentence(pred_tokens: list, true_tokens: list) -> (int, int):
    """
    Calculates precision and coverage of tokens.
    Based on the Longest Common Subsequence Algorithm
    to evaluate pred_tokens and true_tokens, with the difference of
    not considering spaced substrings as matches.

    Examples
    --------
    >>> evaluate_sentence(["Oi", ":)"], ["Oi", ":)"])
    (2, 0, 0)

    Parameters
    ----------
    pred_tokens: list
        List of tokens generated by the tokenizer
    true_tokens: list
        List of true tokens

    Returns
    -------
    (int, int, int)
        True positive, false positives, false negatives
    """

    true_positives = longest_common_token_sequence(pred_tokens, true_tokens)
    false_positives = len(pred_tokens) - true_positives
    false_negatives = len(true_tokens) - true_positives

    return true_positives, false_positives, false_negatives
