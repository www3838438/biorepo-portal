#!/bin/sh

python3 /opt/app/manage.py migrate --noinput
python3 /opt/app/manage.py collectstatic --noinput
python3 /opt/app/manage.py loaddata api/fixtures/demo_data.json

cd /opt/app/ || exit

if [ "$(ls -A /opt/app)" ]; then
    exec gunicorn -b 0.0.0.0:8000 -w 5 brp.wsgi
fi
