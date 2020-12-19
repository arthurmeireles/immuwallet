DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'immuwallet',
        'USER': 'postgres',
        'PASSWORD': 'pgadmin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
