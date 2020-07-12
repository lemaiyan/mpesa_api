from django.conf import settings

from mpesa_api.core.models import AuthToken
from mpesa_api.util.http import post


def send_b2c_request(amount, phone_number, transaction_id, occassion=""):
    """
    seds a b2c request
    :param amount:
    :param phone_numer:
    :return:
    """
    url = f"{settings.MPESA_URL}/mpesa/b2c/v1/paymentrequest"
    headers = {
        "Authorization": "Bearer {}".format(AuthToken.objects.get_token("b2c"))
    }
    request = dict(
        InitiatorName=settings.B2C_INITIATOR_NAME,
        SecurityCredential=settings.B2C_SECURITY_TOKEN,
        CommandID=settings.B2C_COMMAND_ID,
        Amount=str(amount),
        PartyA=settings.B2C_SHORTCODE,
        PartyB=str(phone_number),
        Remarks="record-{}".format(str(transaction_id)),
        QueueTimeOutURL=settings.B2C_QUEUE_TIMEOUT_URL,
        ResultURL=settings.B2C_RESULT_URL,
        Occassion=occassion,
    )

    response = post(url=url, headers=headers, data=request)
    return response.json()
