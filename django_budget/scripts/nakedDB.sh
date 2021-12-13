#!/bin/bash

echo "No turning back, deleting the database"

# python3 -m webbrowser -n https://stackoverflow.com &

sensible-browser http://127.0.0.1:8000/admin/budget &

# ps -aux
# sudo kill 12345

rm db.sqlite3

python3 manage.py makemigrations

python3 manage.py migrate

DJANGO_SUPERUSER_PASSWORD=2JDYuSf4ttHZgFB \
python3 manage.py createsuperuser --email admin@example.com --username admin --no-input

python3 manage.py runserver