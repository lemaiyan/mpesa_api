from django.conf import settings
from util.http import get


def get_token():
    """
    fetch a new token
    :return:
    """
    url = settings.GENERATE_TOKEN_URL
    headers = {"Authorization": "Basic {}".format(settings.MPESA_APP_AUTHTOKEN)}
    response = get(url, headers)
    return response.json()

