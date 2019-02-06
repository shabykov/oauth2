FROM python:3.6

RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev net-tools nmap

RUN pip install -U pip setuptools
RUN pip install uwsgi
RUN mkdir -p /var/log/uwsgi/

ADD weboauth2 app/weboauth2

COPY secrets.json app/
COPY requirements.txt app/weboauth2/
COPY uwsgi.ini app/weboauth2/
COPY docker/weboauth2-entrypoint.sh app/weboauth2/

WORKDIR app/weboauth2

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE config.settings.docker

ENTRYPOINT ["bash", "weboauth2-entrypoint.sh"]