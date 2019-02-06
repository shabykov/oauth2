#!/usr/bin/env bash

python manage.py makemigrations --settings=config.settings.docker
python manage.py migrate --settings=config.settings.docker