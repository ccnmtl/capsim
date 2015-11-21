#!/bin/bash

cd /app/
/ve/bin/python manage.py migrate --noinput --settings=capsim.settings_docker
/ve/bin/python manage.py collectstatic --noinput --settings=capsim.settings_docker
/ve/bin/python manage.py compress --settings=capsim.settings_docker
exec /ve/bin/gunicorn --env \
  DJANGO_SETTINGS_MODULE=capsim.settings_docker \
  capsim.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
