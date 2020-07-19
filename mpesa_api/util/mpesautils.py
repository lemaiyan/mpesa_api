from django.conf import settings
import base64
from mpesa_api.util.http import get


def get_token(type):
    """
    fetch a new token
    :param: type: whether we are fetching token for B2C or C2B
    :return: JSON
    """
    url = f"{settings.MPESA_URL}/oauth/v1/generate?grant_type=client_credentials"
    concat_str = "{}:{}".format(
        settings.MPESA_C2B_ACCESS_KEY, settings.MPESA_C2B_CONSUMER_SECRET
    )
    auth_token = encode_str_to_base_64(concat_str)
    if type.lower() == "b2c":
        concat_str = "{}:{}".format(
            settings.MPESA_B2C_ACCESS_KEY, settings.MPESA_B2C_CONSUMER_SECRET
        )
        auth_token = encode_str_to_base_64(concat_str)
    headers = {"Authorization": "Basic {}".format(auth_token)}
    response = get(url, headers)
    return response.json()


def encode_str_to_base_64(str_to_encode):
    """
    Encodes the a given string to base64
    :param str_to_encode: str to encode
    :return: base64 encoded str
    """
    return base64.urlsafe_b64encode(str_to_encode.encode("UTF-8")).decode(
        "ascii"
    )
