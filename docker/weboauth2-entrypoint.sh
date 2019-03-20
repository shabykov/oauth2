#!/usr/bin/env bash

#while ! nc -z postgres 5432 ; do echo postgresql service is closed; sleep 1; done

uwsgi --ini uwsgi.ini

bash django_cmd_migrate.sh

sleep infinity