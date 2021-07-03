import os
import tempfile

from dante_tokenizer.data.load import read_tokens_from_csv


def test_test_tokens_from_csv():

    # Generate dummy data
    temp_fd, temp_filename = tempfile.mkstemp()

    try:
        with os.fdopen(temp_fd, "w") as tmp:
            tmp.write("tweet_id,text,etc\n")
            tmp.write("1,'text1',a\n")
            tmp.write('2,"text2",a\n')
            tmp.write("3,text3,a\n")
            tmp.write("4,te'x't4,a\n")

        sent_ids, sent_texts = read_tokens_from_csv(temp_filename)

        assert len(sent_ids) == 4
        assert len(sent_texts) == 4

    finally:
        os.remove(temp_filename)
