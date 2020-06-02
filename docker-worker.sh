#!/bin/bash

exec ./ve/bin/celery worker --settings=capsim.settings_docker
