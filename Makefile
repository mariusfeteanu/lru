.DEFAULT_GOAL := test

init:
	pipenv --three install --dev
	pipenv check
	pipenv shell

analyze:
	pylint lru
	pylint test_lru
	flake8 lru.py
	flake8 test_lru.py

test: analyze
	python -m pytest -s

data:
	mkdir -p ./data/
	if [[ ! -f ./data/pageviews ]]; then curl https://dumps.wikimedia.org/other/pageviews/2019/2019-02/pageviews-20190201-000000.gz -o ./data/pageviews.gz; fi;
	if [[ ! -f ./data/pageviews ]]; then gunzip ./data/pageviews.gz; fi;

perf: data
	python -m perf_lru

profile: data
	python -m profile_lru

all: analyze test
