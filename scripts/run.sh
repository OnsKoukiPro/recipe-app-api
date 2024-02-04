#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput #collects all the static files and puts them in the configured static files dir to make them accesible for the nginx proxy
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
#running the uwsgi service, running it in the tcp socket port 9000, used by the nginx server to connect to the app
#running on 4 workers
#module , to run the wsgi file in the app dir