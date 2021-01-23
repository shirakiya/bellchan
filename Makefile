RUN_CONTEXT ?= docker-compose run --rm bot

run:
	docker-compose up

bash:
	$(RUN_CONTEXT) bash

lint: lint/flake8

lint/flake8:
	$(RUN_CONTEXT) flake8 .
