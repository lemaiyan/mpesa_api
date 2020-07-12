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

Add the following in your settings file get the values from [https://developer.safaricom.co.ke](https://developer.safaricom.co.ke)

```python
...
# B2C (Bulk Payment) Configs
# see https://developer.safaricom.co.ke/test_credentials
# https://developer.safaricom.co.ke/b2c/apis/post/paymentrequest

#Consumer Key
MPESA_B2C_ACCESS_KEY = 'bmmI3UPlJa3pt8GqDG1Fu9D7cKy5YooF'
#Consumer Secret
MPESA_B2C_CONSUMER_SECRET = 'dee8AzvwJKNoZ3YW'
# This is the encryption of the scurity Credentials I used the Developer site to encrypt it.
B2C_SECURITY_TOKEN = 'E3Lw64xJ+/ayn1StCP9nu/ObqzgPgCf1IG6JEiubn91QOxkc4u8F0h9NdgjGHaWDHYDEaWxdxqd7uh3ZBsZCrPCm+8ckz8BX/Fqu/x0jOnKzEWwUdbdbFm+hV2q5HJY/EWIq6lnJQeCahkte0TQ6OoVzKyRIUsD4F+pkIIaMkjvqK5mcFWlZQIhoodXd9oBtlo7GWbcYNOjO1+GatYCtVgvjmfWHqI5k4PV/3zjNxvIcTmlB4Ao43fRvXwkRQsvc+8QOUDb6JDO0uF0UhAtz53QLdVmMNmldRoy/nEQ+QrKheY4PhXxnwhrIkFtzWhEG8AhWZjz/Ck4Kr6ePepNEuA=='
#InitiatorName
B2C_INITIATOR_NAME = 'testapi409'
# CommandID
B2C_COMMAND_ID = 'SalaryPayment'
#PartyA
B2C_SHORTCODE = '601409'
# this is the url where Mpesa  will post in case of a time out. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_QUEUE_TIMEOUT_URL = 'http://mpesa.ngrok.io/mpesa/b2c/timeout'
# this is the url where Mpesa will post the result. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_RESULT_URL = 'http://mpesa.ngrok.io/mpesa/b2c/result'
# this is the url where we post the B2C request to Mpesa. Replace this with the url you get from safaricom after you have passed the UATS
B2C_URL = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

# C2B (Paybill) Configs
# See https://developer.safaricom.co.ke/c2b/apis/post/registerurl

#Consumer Secret
MPESA_C2B_ACCESS_KEY = 'bmmI3UPlJa3pt8GqDG1Fu9D7cKy5YooF'
# Consumer Key
MPESA_C2B_CONSUMER_SECRET = 'dee8AzvwJKNoZ3YW'
# Url for registering your paybill replace it the url you get from safaricom after you have passed the UATS
C2B_REGISTER_URL = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
#ValidationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_VALIDATE_URL = 'http://mpesa.ngrok.io/mpesa/c2b/validate'
#ConfirmationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_CONFIRMATION_URL = 'http://mpesa.ngrok.io/mpesa/c2b/confirmation'
#ShortCode (Paybill)
C2B_SHORT_CODE = '600000'
#ResponseType
C2B_RESPONSE_TYPE = 'Completed'

# C2B (STK PUSH) Configs
# https://developer.safaricom.co.ke/lipa-na-m-pesa-online/apis/post/stkpush/v1/processrequest

# Url for sending the STK push request replace it the url you get from safaricom after you have passed the UATS
C2B_ONLINE_CHECKOUT_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
# Where the Mpesa will post the response
#replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'http://mpesa.ngrok.io/mpesa/c2b/online_checkout/callback'
# TransactionType
C2B_TRANSACTION_TYPE = 'CustomerPayBillOnline'
# The Pass Key provided by Safaricom when you pass UAT's
# See https://developer.safaricom.co.ke/test_credentials
C2B_ONLINE_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
# Your Paybill
C2B_ONLINE_SHORT_CODE = '174379'

# URL generate OAUTH token
# See https://developer.safaricom.co.ke/oauth/apis/get/generate-1
GENERATE_TOKEN_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# number of seconds from the expiry we consider the token expired the token expires after an hour
# so if the token is 600 sec (10 minutes) to expiry we consider the token expired.
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

You can view your transaction under django Admin.

