#!/bin/bash

echo "No turning back, deleting the database"

rm db.sqlite3

echo "Cleaning Migrations"

rm ./budget/migrations/*

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser --email admin@example.com --username admin --password 2JDYuSf4ttHZgFB

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver