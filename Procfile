release: python manage.py migrate
web: gunicorn core.wsgi --log-file -
worker: celery --app core worker --loglevel=INFO -f logs/celery.log
