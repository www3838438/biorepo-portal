#!/bin/bash

cd /opt/app

./manage.py test portal
./manage.py test api
