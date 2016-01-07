import os
import json
from base import *  # noqa
import environ

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env('{0}.env'.format(env('APP_ENV')))  # reading .env file

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

TIME_ZONE = env('TIME_ZONE', default='America/New_York')
DEBUG = env.bool('DEBUG')

#####################################
# Database and Caching
#####################################

DATABASES = {
    'default': env.db(),
}

CACHES = {
    'default': env.cache(),
}

#####################################
# General Django Settings
#####################################

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_SUBJECT_PREFIX = '[brp]'
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME')
SECRET_KEY = env('SECRET_KEY')

#####################################
# eHB Settings
#####################################

SERVICE_CLIENT_SETTINGS = {
    "API_KEY": env('SERVICE_CLIENT_API_KEY'),
    "APP_URL": env('SERVICE_CLIENT_APP_URL'),
    "HOST": env('SERVICE_CLIENT_HOST'),
    "ISSECURE": env.bool('SERVICE_CLIENT_ISSECURE'),
    "ROOT_PATH": env('SERVICE_CLIENT_ROOT_PATH'),
    "SELF_ROOT_PATH": env('SERVICE_CLIENT_SELF_ROOT_PATH')
}

PROTOCOL_PROPS = {
    "CLIENT_KEY": {
        "key": env('PROTOCOL_PROPS_CLIENT_KEY')
    },
    "IMMUTABLE_KEYS": {
        "length": env.int('IMMUTABLE_KEY_LENGTH'),
        "seed": env.int('IMMUTABLE_KEY_SEED')
    }
}

#####################################
# LDAP Integration
#####################################
# LDAP Authentication Backend -- LDAP_BIND_PASSWORD and LDAP_SERVER_URI are
# defined in local_settings.py
LDAP = {}
LDAP['DEBUG'] = env.bool('LDAP_DEBUG')
LDAP['PREBINDDN'] = env.str('LDAP_PREBINDDN')
LDAP['SEARCHDN'] = env.str('LDAP_SEARCHDN')
LDAP['SEARCH_FILTER'] = env.str('LDAP_SEARCH_FILTER')
LDAP['SERVER_URI'] = env('LDAP_SERVER_URI')
LDAP['PREBINDPW'] = env('LDAP_PREBINDPW')

#####################################
# Raven Logging
#####################################

if not DEBUG:
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {
        'dsn': env('RAVEN_DSN'),
    }

#####################################
# Static Paths
#####################################
STATIC_URL = '/static/'

if FORCE_SCRIPT_NAME:
    ADMIN_MEDIA_PREFIX = os.path.join(
        FORCE_SCRIPT_NAME, ADMIN_MEDIA_PREFIX[1:])
    STATIC_URL = os.path.join(FORCE_SCRIPT_NAME, STATIC_URL[1:])
    MEDIA_URL = os.path.join(FORCE_SCRIPT_NAME, MEDIA_URL[1:])
    LOGIN_URL = os.path.join(FORCE_SCRIPT_NAME, LOGIN_URL[1:])
    LOGOUT_URL = os.path.join(FORCE_SCRIPT_NAME, LOGOUT_URL[1:])
    LOGIN_REDIRECT_URL = os.path.join(
        FORCE_SCRIPT_NAME, LOGIN_REDIRECT_URL[1:])
