from .base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': os.environ.get('PG_USER'),
        'PASSWORD': os.environ.get('PG_PASSWORD'),
        'HOST': '127.0.0.1',
    }
}


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Celery
CELERY_BROKER_URL = 'amqp://localhost:5672'