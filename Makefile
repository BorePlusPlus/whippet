init:
	poetry install
	poetry run whippet -y

lint:
	poetry run black --check .

format:
	poetry run black .

test:
	poetry run pytest

dev:
	poetry run ptw

pre-commit: lint test


.PHONY: init lint format test dev pre-commit
