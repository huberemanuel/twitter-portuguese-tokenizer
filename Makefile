install:
	pip3 install -r requirements.txt
	pip install -e .

test:
	pytest

nltk-init:
	python3 -m nltk.downloader punkt

eval-dante:
	python3 -m dante_tokenizer.apps.eval_tokenizers data/tweets_stocks.csv data/dante_tweets1a50.conllu
