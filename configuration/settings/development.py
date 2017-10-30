from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],  # Set to empty string for default.
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Celery
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s module=%(module)s, '
                      'process_id=%(process)d, path=%(pathname)s, environment=%(environment)s, %(message)s'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
}


