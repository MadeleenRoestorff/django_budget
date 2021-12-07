#!/bin/bash

echo "No turning back, deleting the database"

rm db.sqlite3

python3 manage.py makemigrations

python3 manage.py migrate

DJANGO_SUPERUSER_PASSWORD=2JDYuSf4ttHZgFB \
python3 manage.py createsuperuser --email admin@example.com --username admin --no-input

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver