# syntax=docker/dockerfile:1
FROM python:3.9.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update
COPY . /code/
WORKDIR /code
RUN pip install -r docker_setup/requirements.txt