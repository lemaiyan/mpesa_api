import base64
from datetime import datetime

from django.conf import settings

from mpesa_api.core.models import AuthToken
from mpesa_api.util.http import post


def register_c2b_url():
    """
    Register the c2b_url
    :return:
    """
    url = f"{settings.MPESA_URL}/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": "Bearer {}".format(AuthToken.objects.get_token("c2b"))
    }
    body = dict(
        ShortCode=settings.C2B_SHORT_CODE,
        ResponseType=settings.C2B_RESPONSE_TYPE,
        ConfirmationURL=settings.C2B_CONFIRMATION_URL,
        ValidationURL=settings.C2B_VALIDATE_URL,
    )
    response = post(url=url, headers=headers, data=body)
    return response.json()


def process_online_checkout(
    msisdn: int,
    amount: int,
    account_reference: str,
    transaction_desc: str,
    is_paybil=True,
):
    """
    Handle the online checkout
    :param msisdn:
    :param amount:
    :param account_reference:
    :param transaction_desc:
    :param is_paybil: If set to False it means we are make a till transaction
    :return:
    """
    transaction_type = "CustomerPayBillOnline"
    if not is_paybil:
        transaction_type = "CustomerBuyGoodsOnline"

    url = f"{settings.MPESA_URL}/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": "Bearer {}".format(AuthToken.objects.get_token("c2b"))
    }
    timestamp = (
        str(datetime.now())[:-7]
        .replace("-", "")
        .replace(" ", "")
        .replace(":", "")
    )
    password = base64.b64encode(
        bytes(
            "{}{}{}".format(
                settings.C2B_ONLINE_SHORT_CODE,
                settings.C2B_ONLINE_PASSKEY,
                timestamp,
            ),
            "utf-8",
        )
    ).decode("utf-8")
    body = dict(
        BusinessShortCode=settings.C2B_ONLINE_SHORT_CODE,
        Password=password,
        Timestamp=timestamp,
        TransactionType=transaction_type,
        Amount=str(amount),
        PartyA=str(msisdn),
        PartyB=settings.C2B_ONLINE_PARTY_B,
        PhoneNumber=str(msisdn),
        CallBackURL=settings.C2B_ONLINE_CHECKOUT_CALLBACK_URL,
        AccountReference=account_reference,
        TransactionDesc=transaction_desc,
    )
    response = post(url=url, headers=headers, data=body)
    return response.json()
