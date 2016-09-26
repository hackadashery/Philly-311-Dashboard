web: gunicorn dash311:app --log-file -
worker: celery -A /scripts/download.py worker -B -E --loglevel=info