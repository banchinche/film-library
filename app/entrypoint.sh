#!/bin/sh
if [ $FLASK_APP = "wsgi.py" ]; then
    flask db init
    flask db migrate
    flask db upgrade
else
  echo "Smth went wrong with migrations..."
fi