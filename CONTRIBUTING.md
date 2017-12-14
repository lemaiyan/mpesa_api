## Contributing.

# Set Up
First you have to run the application to do so clone the repository and make sure you have docker
installed and run the command `docker-compose up` this will download all the relevant docker images 
and start the services and also the celery worker. 

to be able to receive callbacks from Safaricom you need to set up a tunnel and for this we will use
`ngrok` you can download it here[https://ngrok.com/](https://ngrok.com/) once you have set it up
run the following command to start a tunnel to our app 
```bash
ngrok http 8090
# or if you have the paid version and substitute the name mpesa with your desired subdomain name
ngrok http --subdomain=mpesa 8090
```
copy the http endpoint _(say the end is `http://mpesa.ngrok.io`)_ and update the following configs 

```python
B2C_QUEUE_TIMEOUT_URL = 'http://mpesa.ngrok.io/mpesa/b2c/timeout'
B2C_RESULT_URL = 'http://mpesa.ngrok.io/mpesa/b2c/result'
C2B_VALIDATE_URL = 'http://mpesa.ngrok.io/mpesa/c2b/validate'
C2B_CONFIRMATION_URL = 'http://mpesa.ngrok.io/mpesa/c2b/confirmation'
C2B_ONLINE_CHECKOUT_CALLBACK_URL = 'http://mpesa.ngrok.io/mpesa/c2b/online_checkout/callback'
```

and with that you're set to begin development and testing

## Workflow

To add new changes make sure you do that on a separate branch and once done create pull request this 
will be reviewed and if all is okay it will be merged to master. Also make sure you have update the 
documentation if the changes you're making requires such.