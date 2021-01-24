RUN_CONTEXT ?= docker-compose run --rm bot

start:
	docker-compose up

run:
	$(RUN_CONTEXT) python run.py

bash:
	$(RUN_CONTEXT) bash

lint: lint/flake8

lint/flake8:
	$(RUN_CONTEXT) flake8 .
