FROM python:3.7-alpine
MAINTAINER Kateryna


COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock/ Pipfile.lock

RUN apk update \
    && apk add --no-cache postgresql-client python3 \
    && apk add --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev \
    && pip3 install --no-cache-dir -U pip pipenv \
    && pip3 install pipenv \
    && pipenv install --system --deploy \
    && apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

