# syntax=docker/dockerfile:1
FROM python:3.9.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN sudo apt-get -y update
RUN sudo apt-get -y install sqlite3 libsqlite3-dev
COPY . /code/
WORKDIR /code
RUN pip3 install -r docker_setup/requirements.txt
