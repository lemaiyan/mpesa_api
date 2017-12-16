[![CircleCI](https://circleci.com/gh/lemaiyan/mpesa_api.svg?style=svg)](https://circleci.com/gh/lemaiyan/mpesa_api)


## Installation

`pip install mpesa-api` or 
`pip install -e git+https://github.com/lemaiyan/mpesa_api.git#egg=mpesa_api`


## Requirements 

- Python 3.4+
- Django 1.11.7+
- Celery 4.1.0+
- djangorestframework 3.7.3+
- requests 2.18.4+

## Setup

Add the following in the `urls.py`
```python
urlpatterns = [
    ...
    url(r'^mpesa/', include('mpesa_api.core.urls', 'mpesa')),
    ...
]
```
Add the following to installed apps

```python
INSTALLED_APPS = [
    ...
    'mpesa_api.core',
    'mpesa_api.util',
    ...
```

Add the following in your settings file get the values from [https://developer.safaricom.co.ke](https://developer.safaricom.co.ke)

```python
...
MPESA_B2C_ACCESS_KEY = 'Mpesa b2c access Key'
MPESA_B2C_CONSUMER_SECRET = 'Mpesa b2c consumer secret'
MPESA_C2B_ACCESS_KEY = 'Mpesa c2b access Key'
MPESA_C2B_CONSUMER_SECRET = 'Mpesa c2b consumer secret'
B2C_SECURITY_TOKEN = 'b2c security token'
B2C_INITIATOR_NAME = 'b2c initiator name'
B2C_COMMAND_ID = 'Sb2c command id'
B2C_SHORTCODE = 'b2c shortcode'
B2C_QUEUE_TIMEOUT_URL = 'b2c queue timeout url'
B2C_RESULT_URL = 'b2c result url'

C2B_REGISTER_URL = 'c2b register url'
C2B_VALIDATE_URL = 'c2b validate url'
C2B_CONFIRMATION_URL = 'c2b confirmation url'
C2B_SHORT_CODE = 'c2b short code'
C2B_RESPONSE_TYPE = 'Completed'

C2B_ONLINE_CHECKOUT_URL = 'c2b online checkout url'
C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'online checkout callback url'
C2B_TRANSACTION_TYPE = 'CustomerPayBillOnline'
C2B_ONLINE_PASSKEY = 'c2b online passkey'
C2B_ONLINE_SHORT_CODE = 'c2b online short code'

# Urls
GENERATE_TOKEN_URL = 'auth url'
B2C_URL = 'b2c url'

# number of seconds from the expiry we consider the token expired 
# the token expires after an hour 
TOKEN_THRESHOLD = 600

...
```
### Celery

After adding the mpesa settings also add the celery settings which is the path url to your rabbitmq the value below 
is for when you're using the default else add the appropriate URL
```python
...
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
...
```
To fully configure celery add `celery.py` in your django folder where your `settings.py` and 
`wsgi.py` resides with the following code
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# in this case the settings we are using are located in config.settings
# so make sure you point to the correct path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery('config')

# Using a string here means the worker don't have to serialize
# the config object to child processes.
# - namespace='CELERY' means all celery-related config keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

in the `__init__.py` file located in the same location add the following code
```python
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
```

In the root of the project folder add `celery.sh` file this is what is used to run the `celery workers`
and where we register the queues we have defined for the tasks we have. add the following code
```bash
#!/usr/bin/env bash
celery -A config worker -c 5 --loglevel=info -Q b2c_result,b2c_request,celery,c2b_confirmation,c2b_validation,online_checkout_request,online_checkout_callback
```
make sure you make this file executable and run it to run the workers.


## Usage

Once you're done with the set up you need to be able to make calls to MPESA API's in your `.py` file
where you want to make the calls add the following line
```python
from mpesa_api.core.mpesa import Mpesa
```
The `Mpesa` class containts static methods to intereact with the MPESA API's. They initiate the calls
and also keeps track of the callbacks and the values are stored in the database for retrieval. 
Below are some samples
```python
Mpesa.b2c_request(254700000000, 100) # starts a b2c payment
Mpesa.c2b_register_url() # registers the validate and confirmation url's for b2c
# starts online checkout on given number 
Mpesa.stk_push(254700000000, 100, account_reference='', transaction_desc='')
```

