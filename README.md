[![CircleCI](https://circleci.com/gh/lemaiyan/mpesa_api.svg?style=svg)](https://circleci.com/gh/lemaiyan/mpesa_api)
##Installation

`pip install mpesa-api` or 
`pip install -e git+https://github.com/lemaiyan/mpesa_api.git#egg=mpesa_api`

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
MPESA_APP_ACCESS_KEY = 'Mpesa App access Key'
MPESA_APP_CONSUMER_SECRET = 'Mpesa app consumer secret'
MPESA_APP_AUTHTOKEN = 'mpesa auth token'
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