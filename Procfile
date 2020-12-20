web: daphne immuwallet.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A immuwallet.apps.api worker -B -l INFO
