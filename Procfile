web: daphne civiwiki.asgi:channel_layer --port $PORT --bind 172.0.0.1 -v2
worker: python manage.py runworker -v2
worker: celery -A civiwiki worker --app=civiwiki.celery:app -l info
