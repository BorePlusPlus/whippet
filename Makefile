install:
	poetry install

init: install
	poetry run whippet -y

lint:
	poetry run black --check .
	poetry run mypy -p whippet

format:
	poetry run black .

test:
	poetry run pytest

dev:
	poetry run ptw

check: lint test

pre-commit: check

ci: check


.PHONY: install init lint format test dev check pre-commit ci
