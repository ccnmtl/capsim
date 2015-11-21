#!/bin/bash

exec /ve/bin/python manage.py celery worker --settings=capsim.settings_docker
