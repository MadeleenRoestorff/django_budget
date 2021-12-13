#!/bin/bash

# python3 -m webbrowser -n https://stackoverflow.com &

sensible-browser http://127.0.0.1:8000/admin/budget &

# ps -aux
# sudo kill 12345

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

