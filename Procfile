web: gunicorn wsgi --log-file -

#NOTE: worker dyno is not enabled.
worker: python manage.py celery worker --app=otree.celery.app:app --loglevel=INFO
