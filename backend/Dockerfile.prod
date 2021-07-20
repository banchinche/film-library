#base image
FROM python:3.9

# workdir setting
WORKDIR /usr/src/app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:backend/"


# install dependencies
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
COPY backend/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

#copying files
COPY . /usr/src/app/
# CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "manage:app"]

# entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]