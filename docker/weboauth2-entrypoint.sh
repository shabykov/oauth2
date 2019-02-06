#!/usr/bin/env bash

#while ! nc -z postgres 5432 ; do echo postgresql service is closed; sleep 1; done

uwsgi --ini uwsgi.ini

python manage.py migrate --settings=config.settings.docker

sleep infinity