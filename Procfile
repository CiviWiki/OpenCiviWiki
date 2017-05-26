web: daphne civiwiki.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
worker: celery -A civiwiki worker --app=civiwiki.celery:app -l info
