FROM python:3.8

COPY / /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}/app

RUN pip install -r app/requirements.txt
