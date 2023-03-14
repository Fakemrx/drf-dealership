#!/bin/sh

echo "--------------- Launching PSQL ---------------"
if [ "$DATABASE" = "postgres" ]
  then
    echo "Waiting for psql"

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
    done

    echo "--------------- PSQL started ---------------"
fi

echo "--------------- Running migrations ---------------"
python manage.py migrate
echo "--------------- Migrations done ---------------"

echo "--------------- Creating default superuser ---------------"
python manage.py createsuperuser --noinput
echo "Username: " $DJANGO_SUPERUSER_USERNAME
echo "Password: " $DJANGO_SUPERUSER_PASSWORD

exec "$@"
