import dj_database_url

from .settings import ALLOWED_HOSTS, DATABASE_HOST

DATABASES = {
    'default': dj_database_url.config(default=f'postgres://postgres:postgres@{DATABASE_HOST}:5432/immuwallet')
}

ALLOWED_HOSTS += "*"
