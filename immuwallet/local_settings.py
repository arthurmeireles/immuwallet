import dj_database_url
from .settings import ALLOWED_HOSTS, INSTALLED_APPS


DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:postgres@127.0.0.1:5432/immuwallet')
}

ALLOWED_HOSTS += "*"
# INSTALLED_APPS += "django_extensions"

DEBUG = True