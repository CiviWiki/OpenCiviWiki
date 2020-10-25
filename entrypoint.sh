#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"


# Collect static files
echo "Collect static files"
python project/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python project/manage.py migrate

# Start server
echo "Starting server"
python project/manage.py runserver 0.0.0.0:8000

# done

exec "$@"
