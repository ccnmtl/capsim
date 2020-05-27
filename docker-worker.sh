#!/bin/bash

exec ./ve/bin/python3 manage.py celery worker --settings=capsim.settings_docker
