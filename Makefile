SHELL = /bin/bash

.PHONY: default help tests docker

APP_NAME ?= load-transmuter
COMMIT_HASH ?= $(shell git rev-parse HEAD | cut -c 1-8)

DOCKER_VOLUME ?= $(shell pwd):/${APP_NAME}
DOCKER_CONTAINER ?= load-transmuter
DOCKER_IMAGE ?= py-load-transmuter

GREEN = \033[0;32m
NOSTYLE = \033[0m

default: test

help:
	@echo "- Use 'make test' (default) to run all tests and generate a coverage html report"
	@echo "- Use 'make test-only' to only run all tests"
	@echo "- Use 'make docker-build' to generate the docker image"
	@echo -e "  Current IMAGE: '${DOCKER_IMAGE}:${COMMIT_HASH}'"
	@echo "- Use 'make docker' to generate and run the docker container"
	@echo -e "  Current CONTAINER: '${DOCKER_CONTAINER}'"

test-only:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "not in env. Run 'source .venv/bin/activate'"; \
		exit 1; \
	else \
		python -m coverage run -m pytest; \
	fi

test: test-only
	@python -m coverage report -m
	@python -m coverage html
	@echo -e "Check: " $(shell pwd)"/htmlcov/index.html"

docker-build:
	@echo -e "$(GREEN)Building Docker Image...$(NOSTYLE)"
	@docker build --tag ${APP_NAME}:${COMMIT_HASH} .
	@echo -e "$(GREEN)Done$(NOSTYLE)"

docker:
	@docker run -it --name $(DOCKER_CONTAINER) -v $(DOCKER_VOLUME) $(DOCKER_IMAGE)

