#!/bin/bash

cd /var/www/capsim/capsim/
exec python manage.py celery worker --settings=capsim.settings_docker
