from django.conf import settings

from mpesa_api.util.http import get


def get_token(type):
    """
    fetch a new token
    :param: type: whether we are fetching token for B2C or C2B
    :return: JSON
    """
    url = settings.GENERATE_TOKEN_URL
    auth_token = settings.MPESA_B2C_AUTHTOKEN
    if type.lower() == 'c2b':
        auth_token = settings.MPESA_C2B_AUTHTOKEN
    headers = {"Authorization": "Basic {}".format(auth_token)}
    response = get(url, headers)
    return response.json()

