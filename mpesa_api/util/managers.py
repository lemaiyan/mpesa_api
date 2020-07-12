import time

from django.conf import settings
from django.db import models

from mpesa_api.util.mpesautils import get_token


class AuthTokenManager(models.Manager):
    """
    Auth manager token
    """

    def get_token(self, type):
        current_time = int(time.time())
        if self.filter(type=type.lower()).count() == 0:
            # means we don't have a record yet so we create
            token = get_token(type.lower())
            access_token = token["access_token"]
            expires = int(time.time()) + int(token["expires_in"])
            self.create(
                access_token=access_token,
                expires_in=expires,
                type=type.lower(),
            )
            return access_token
        else:
            # check if it's expired if it update
            obj = self.get(type=type.lower())
            if current_time > (obj.expires_in - settings.TOKEN_THRESHOLD):
                token = get_token(type.lower())
                access_token = token["access_token"]
                expires = int(time.time()) + int(token["expires_in"])
                self.filter(type=type.lower()).update(
                    access_token=access_token,
                    expires_in=expires,
                    type=type.lower(),
                )
                return access_token
            else:
                return obj.access_token
