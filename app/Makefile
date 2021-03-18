.PHONY: style check-style start install develop test load-test
style:
	# apply opinionated styles
	@black api
	@isort api

	# tests are production code too!
	@black tests
	@isort tests

check-style:
	@black api --check
	@flake8 orion --count --show-source --statistics --ignore=E203,W503

start:
	@bash bin/run.sh

install:
	@pip3 install -r requirements/common.txt

develop:
	@pip3 install -r requirements/common.txt -r requirements/develop.txt

test:
	@pytest-3 tests

load-test:
	@locust -f tests/load/locustfiles/api.py
