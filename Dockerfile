FROM python:3.9-alpine

MAINTAINER Hundeyin Oluwadamilola

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-deps \
	gcc libc-dev linux-headers postgresql-dev musl-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-deps

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user

USER user