install:
	pip3 install -r requirements.txt
	pip install -e .

test:
	python -m pytest

nltk-init:
	python3 -m nltk.downloader punkt

eval-dante:
ifdef debug
	python3 -m dante_tokenizer.apps.eval_tokenizers data/tweets_stocks.csv data/dante_tweets1a50.conllu --debug
else
	python3 -m dante_tokenizer.apps.eval_tokenizers data/tweets_stocks.csv data/dante_tweets1a50.conllu
endif

create-conllu:
ifdef csv_path
	python3 -m dante_tokenizer.apps.csv_to_conllu $(csv_path)
endif

