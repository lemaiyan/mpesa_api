from django.db import models
from util.managers import AuthTokenManager


class AuthToken(models.Model):
    """Handles AuthTokens"""
    access_token = models.CharField(max_length=40);
    expires_in = models.BigIntegerField()
    objects = AuthTokenManager()

    def __str__(self):
        return self.access_token

    class Meta:
        db_table ='tbl_access_token'




