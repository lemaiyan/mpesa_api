from mpesa_api.core.models import B2CRequest, OnlineCheckout
from mpesa_api.util import exceptions, c2butils
from decimal import Decimal
import uuid


class Mpesa:
    """
    Class that wraps the given mpesa functionality
    """

    @staticmethod
    def b2c_request(phone, amount):
        """
        Initiate a B2C Request
        :param phone: user phone to send the money to e.g. e.g. 254700000000
        :param amount: amount to be credited to the users MPESA wallet
        :return: B2CRequest object
        """
        try:
            return B2CRequest.objects.create(
                phone=int(phone), amount=Decimal(str(amount))
            )
        except Exception as ex:
            raise exceptions.B2CMpesaError(str(ex))

    @staticmethod
    def c2b_register_url():
        """
        Registers the validation and confirmation urls for paybill as defined in the settings file
        using C2B_CONFIRMATION_URL and C2B_VALIDATE_URL
        :return: json
        """
        try:
            return c2butils.register_c2b_url()
        except Exception as ex:
            raise exceptions.UrlRegisterMpesaError(str(ex))

    @staticmethod
    def stk_push(phone, amount, account_reference, is_paybill=True):
        """
        Initiates stk Push transaction
        Please note if you had registered the c2b urls this transaction will also be subjected to
        validation and confirmation.
        Once the transaction is complete or fails the result will be sent to the
        C2B_ONLINE_CHECKOUT_CALLBACK_URL as defined in the settings
        :param phone: user phone to start the stk push e.g. 254700000000
        :param amount: amount to be deducted from the users MPESA wallet
        :param account_reference: the message that get shown to the user on the checkout USSD message
        :return: OnlineCheckout object
        """
        try:
            return OnlineCheckout.objects.create(
                phone=int(phone),
                amount=Decimal(str(amount)),
                account_reference=account_reference,
                transaction_description=uuid.uuid4().hex,
                is_paybill=is_paybill
            )
        except Exception as ex:
            raise exceptions.StkPushMpesaError(str(ex))
