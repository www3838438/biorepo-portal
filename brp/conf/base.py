import os
import datetime

# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *  # noqa
from django.core.exceptions import ImproperlyConfigured

# Import the project module to calculate directories relative to the module
# location.
PROJECT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
PROJECT_ROOT, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)

INSTALLED_APPS = (

    'brp',

    # built-in Django stuff
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'south',

    # third party stuff
    'registration',
    'ehb_client.requests',
    'session_security',
    'rest_framework',
    'rest_framework.authtoken',
    'markdown_deux',

    # project apps in biorepo-portal/apps
    'portal',
    'accounts',
)

# ------------------------------------
# ADMINISTRATIVE
# ------------------------------------
SEND_BROKEN_LINK_EMAILS = False

INTERNAL_IPS = ('127.0.0.1', '::1')

EMAIL_SUBJECT_PREFIX = '[Bio-repository Portal] '

IGNORABLE_404_ENDS = ('robots.txt', 'favicon.ico')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

FORCE_SCRIPT_NAME = ''

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_ETAGS = True

# ------------------------------------
# STATIC AND MEDIA
# ------------------------------------

# The application's static files should be placed in the STATIC_ROOT in
# addition to other static files found in third-party apps. The MEDIA_ROOT
# is intended for user uploaded files.
#

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, PROJECT_MODULE_NAME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, '_site/static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# THIS DOES NOT APPEAR TO BE USED
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ()

# ------------------------------------
# URLS
# ------------------------------------

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/welcome/'

ROOT_URLCONF = 'brp.conf.urls'

# SITEAUTH_ALLOW_URLS = (
#     r'^log(in|out)/',
#     r'^password/reset/',
#     r'^accounts/(register|verify)/',
# )

SITEAUTH_DENY_URLS = (
    r'^accounts/moderate/+',
)
# ------------------------------------
# MIDDLEWARE
# ------------------------------------
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'siteauth.middleware.SiteAuthenticationMiddleware',
    'accounts.middleware.CheckEulaMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

# ------------------------------------
# TEMPLATES
# ------------------------------------

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, PROJECT_MODULE_NAME, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'brp.context_processors.static'
)

# ------------------------------------
# LOGGING
# ------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/debug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/requests.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'ehb': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/ehb.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'ehb_client.requests.external_record_request_handler': {
            'handlers': ['ehb'],
            'propagate': False
        },
        'portal': {
            'handlers': ['ehb'],
            'propagate': True
        }
    }
}


# ------------------------------------
# AUTHENTICATION
# ------------------------------------
AUTHENTICATION_BACKENDS = (
    'portal.accounts.backends.LdapBackend',

)

# django auth user profile integration
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# django-registration
REGISTRATION_BACKENDS = {
    'default': 'accounts.backends.DefaultBackend',
}
REGISTRATION_ACTIVATION_DAYS = 0
REGISTRATION_MODERATION = True

ADMINS = (
    ('Tyler Rivera', 'riverat2@email.chop.edu'),
)
MANAGERS = ADMINS

ACCOUNT_MODERATORS = ADMINS

#
# SESSION
#

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#
# CACHE
#

# For production environments, the memcached backend is highly recommended
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'brp',
        'VERSION': 1,
    }
}

CACHE_MIDDLEWARE_SECONDS = 60 * 30  # 30 minutes

# This is not necessary to set if the above `KEY_PREFIX` value is set since
# the `KEY_PREFIX` namespaces all cache set by this application
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# The primary key of the ``Site`` object for the Sites Framework
SITE_ID = 1

PLUGINS = {}

SESSION_SECURITY_WARN_AFTER = 240
SESSION_SECURITY_EXPIRE_AFTER = 300
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEFAULT_FROM_EMAIL = 'cbmisupport@email.chop.edu'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
}
