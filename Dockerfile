FROM python:3.8

COPY /app /app

COPY /tests /tests

COPY /requirements.txt /requirements.txt

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:7070",  "wsgi:app"]