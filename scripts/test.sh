#!/bin/bash

cd /opt/app

./brp/manage.py test portal
./brp/manage.py test api
