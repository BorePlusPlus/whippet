lint:
	poetry run black --check .

format:
	poetry run black .

test:
	poetry run pytest
