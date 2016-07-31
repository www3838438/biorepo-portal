#!/bin/sh

python /opt/app/manage.py migrate --noinput
python /opt/app/manage.py collectstatic --noinput

cd /opt/app/ || exit

if [ "$(ls -A /opt/app)" ]; then
    exec gunicorn -b 0.0.0.0:8000 -w 5 brp.wsgi
fi
