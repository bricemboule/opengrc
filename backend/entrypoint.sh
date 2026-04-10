#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_rbac || true

gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 3 --timeout 120
