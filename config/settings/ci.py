from .base import *
import os

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
CELERY_BROKER_URL = 'amqp://localhost:5672'