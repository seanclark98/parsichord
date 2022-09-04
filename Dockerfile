FROM python:3.10.6-alpine3.16
LABEL maintainer="seanclark98"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./parsichord /parsichord
WORKDIR /parsichord
EXPOSE 8000

ARG DEV=false
RUN python -m venv /.venv && \
    /.venv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /.venv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /.venv/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/.venv/bin:$PATH"

USER django-user