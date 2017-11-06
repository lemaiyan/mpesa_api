from django.conf import settings
from util.http import post
from core.models import AuthToken
import json


def register_c2b_url():
    """
    Register the c2b_url
    :return:
    """
    url = settings.C2B_REGISTER_URL
    headers = {"Content-Type": 'application/json',
               'Authorization': 'Bearer {}'.format(AuthToken.objects.get_token())}
    body = dict(
        ShortCode=settings.C2B_SHORT_CODE,
        ResponseType=settings.C2B_RESPONSE_TYPE,
        ConfirmationURL=settings.C2B_CONFIRMATION_URL,
        ValidationURL=settings.C2B_VALIDATE_URL
    )
    response = post(url=url, headers=headers, data=json.dumps(body))
    return response.json()

