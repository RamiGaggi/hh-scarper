install:
	@poetry install

runserver:
	@poetry run python manage.py runserver 0.0.0.0:8000

migrations:
	@poetry run python manage.py makemigrations

migrate: migrations
	@poetry run python manage.py migrate

lint:
	@poetry run flake8

secret-key:
	@poetry run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

test:
	@poetry run pytest hhscarper

test-coverage:
	poetry run pytest hhscarper --cov=hhscarper

coverage-report-xml:
	@poetry run coverage xml

requirements.txt: poetry.lock
	@poetry export --format requirements.txt --output requirements.txt