FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /civi_app

WORKDIR /civi_app

ADD . /civi_app

RUN apt-get update && apt-get install -y git

RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt