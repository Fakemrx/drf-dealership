#!/bin/sh

echo "Trying to launch psql"
if [ "$DATABASE" = "postgres" ]
  then
    echo "Waiting for psql"

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
    done

    echo "Psql started"
fi

python manage.py migrate
python manage.py createsuperuser --noinput

exec "$@"
