FROM python:3.8

COPY / /project

ENV PYTHONPATH=${PYTHONPATH}:${PWD}/project

RUN pip install -r project/requirements.txt && chmod +x /project/app/entrypoint.sh

ENTRYPOINT ["/project/app/entrypoint.sh"]
