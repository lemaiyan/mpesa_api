from django.db import models
from util.mpesautils import get_token
from django.conf import settings
import time


class AuthTokenManager(models.Manager):
    """
    Auth manager token
    """
    def get_token(self):
        current_time = int(time.time())
        if self.count() == 0:
            # means we don't have a record yet so we create
            token = get_token()
            access_token = token['access_token']
            expires = int(time.time()) + int(token['expires_in'])
            self.create(access_token=access_token, expires_in=expires)
            return access_token
        else:
            # check if it's expired if it update
            obj = self.get(pk=1)
            if current_time > (obj.expires_in - settings.TOKEN_THRESHOLD):
                token = get_token()
                #import ipdb;ipdb.set_trace()
                access_token = token['access_token']
                expires = int(time.time()) + int(token['expires_in'])
                self.filter(pk=1).update(access_token=access_token, expires_in=expires)
                return access_token
            else:
                return obj.access_token
