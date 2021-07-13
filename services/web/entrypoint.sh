#!/bin/sh

if [ "$DATABASE" = "movies" ]
then
    echo "Waiting for movies..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db
python manage.py seed_db
exec "$@"