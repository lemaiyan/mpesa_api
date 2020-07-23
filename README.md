[![CircleCI](https://circleci.com/gh/lemaiyan/mpesa_api.svg?style=svg)](https://circleci.com/gh/lemaiyan/mpesa_api)
[![codecov](https://codecov.io/gh/lemaiyan/mpesa_api/branch/master/graph/badge.svg)](https://codecov.io/gh/lemaiyan/mpesa_api)


## Status
As of now the following services are done
* B2C
* C2B
* STK PUSH

The pending services are
* Reversal
* Transaction Status
* Account Balance
* B2B

If you have a free pair of hands let me know.

## Installation

`pip install mpesa-api` or 
`pip install -e git+https://github.com/lemaiyan/mpesa_api.git#egg=mpesa_api`


## Requirements 

- Python 3.8+
- Django 2.1.7+
- Celery 4.1.0+
- djangorestframework 3.7.3+
- requests 2.18.4+
- python-decouple 3.3+

## Setup

Add the following in the `urls.py`
```python
urlpatterns = [
    ...
    path('mpesa/', include('mpesa_api.core.urls', 'mpesa')),
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
Copy the `.env-example` to `.env`. Note the `DB` and `DJANGO` configs are needed when using docker. 
Add the following in your settings file get the values from [https://developer.safaricom.co.ke](https://developer.safaricom.co.ke)

```python
...
# Safaricom Configs

# B2C (Bulk Payment) Configs
# see https://developer.safaricom.co.ke/test_credentials
# https://developer.safaricom.co.ke/b2c/apis/post/paymentrequest

#Consumer Key
MPESA_B2C_ACCESS_KEY = config('MPESA_B2C_ACCESS_KEY')
#Consumer Secret
MPESA_B2C_CONSUMER_SECRET = config('MPESA_B2C_CONSUMER_SECRET')
# This is the encryption of the scurity Credentials I used the Developer site to encrypt it.
B2C_SECURITY_TOKEN =  config('B2C_SECURITY_TOKEN')
#InitiatorName
B2C_INITIATOR_NAME = config('B2C_INITIATOR_NAME')
# CommandID
B2C_COMMAND_ID = config('B2C_COMMAND_ID')
#PartyA
B2C_SHORTCODE = config('B2C_SHORTCODE')
# this is the url where Mpesa  will post in case of a time out. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_QUEUE_TIMEOUT_URL = config('B2C_QUEUE_TIMEOUT_URL')
# this is the url where Mpesa will post the result. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_RESULT_URL = config('B2C_RESULT_URL')
# this is the url where we post the B2C request to Mpesa. Replace this with the url you get from safaricom after you have passed the UATS
MPESA_URL = config('MPESA_URL')

# C2B (Paybill) Configs
# See https://developer.safaricom.co.ke/c2b/apis/post/registerurl

#Consumer Secret
MPESA_C2B_ACCESS_KEY = config('MPESA_C2B_ACCESS_KEY')
# Consumer Key
MPESA_C2B_CONSUMER_SECRET = config('MPESA_C2B_CONSUMER_SECRET')
# Url for registering your paybill replace it the url you get from safaricom after you have passed the UATS
C2B_REGISTER_URL = config('C2B_REGISTER_URL')
#ValidationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_VALIDATE_URL = config('C2B_VALIDATE_URL')
#ConfirmationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_CONFIRMATION_URL = config('C2B_CONFIRMATION_URL')
#ShortCode (Paybill)
C2B_SHORT_CODE = config('C2B_SHORT_CODE')
#ResponseType
C2B_RESPONSE_TYPE = config('C2B_RESPONSE_TYPE')

# C2B (STK PUSH) Configs
# https://developer.safaricom.co.ke/lipa-na-m-pesa-online/apis/post/stkpush/v1/processrequest

#replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_ONLINE_CHECKOUT_CALLBACK_URL = config('C2B_ONLINE_CHECKOUT_CALLBACK_URL')
# The Pass Key provided by Safaricom when you pass UAT's
# See https://developer.safaricom.co.ke/test_credentials
C2B_ONLINE_PASSKEY = config('C2B_ONLINE_PASSKEY')
# Your Short code
C2B_ONLINE_SHORT_CODE = config('C2B_ONLINE_SHORT_CODE', default='')
# your paybill or till number
C2B_ONLINE_PARTY_B = config('C2B_ONLINE_PARTY_B', default='')
# number of seconds from the expiry we consider the token expired the token expires after an hour
# so if the token is 600 sec (10 minutes) to expiry we consider the token expired.
TOKEN_THRESHOLD = config('TOKEN_THRESHOLD')

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
Mpesa.stk_push(254700000000, 100, account_reference='', transaction_desc='', is_paybill=True)
```

You can view your transaction under django Admin.

