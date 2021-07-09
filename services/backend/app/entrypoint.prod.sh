#!/bin/sh

if [ "$POSTGRES_DB" = "practice" ]
then
    echo "Waiting for $POSTGRES_DB database..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "$POSTGRES_DB started."
fi

python manage.py create_db

exec "$@"