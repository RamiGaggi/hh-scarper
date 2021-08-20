release: python manage.py migrate
web: gunicorn hhscarper.wsgi --log-file -
worker: celery -A core worker --loglevel=INFO
