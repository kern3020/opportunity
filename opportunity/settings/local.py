import os

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# override value in base for debugging.
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')
STATIC_ROOT = 'staticfiles' 
STATIC_URL = '/static/'

DATABASES = { 'default': {} }
DATABASES['default'] = dj_database_url.config()

INSTALLED_APPS += ('django_extensions',)
# INSTALLED_APPS += ("debug_toolbar",)
# INTERNAL_IPS = ("127.0.0.1",)
# MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

if DEBUG:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@localhost'
