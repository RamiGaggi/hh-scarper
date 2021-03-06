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
	@poetry run pytest -vv hhscarper --log-cli-level=DEBUG 

test-coverage:
	poetry run pytest hhscarper --cov=hhscarper --cov-report xml

coverage-report:
	@poetry run coverage report

requirements.txt: poetry.lock
	@poetry export --format requirements.txt --output requirements.txt

celery-worker:
	@poetry run celery --app core worker --loglevel=INFO -f logs/celery.log

flower:
	@celery --app core flower

shell:
	poetry run python manage.py shell_plus --print-sql

collectstatic:
	@poetry run python manage.py collectstatic

setup: migrate
	@echo Create a super user
	@poetry run python manage.py createsuperuser
