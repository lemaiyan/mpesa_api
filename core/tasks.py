from __future__ import absolute_import, unicode_literals
from celery import shared_task
from util.b2cutils import send_b2c_request
from core.models import B2CRequest, C2BRequest
from decimal import Decimal


@shared_task(name='core.b2c_call')
def send_b2c_request_task(amount, phone, id):
    """
    task for send a b2c request
    :param amount:
    :param phone:
    :param id:
    :return:
    """
    return send_b2c_request(amount, phone, id)


@shared_task(name='core.handle_b2c_call_response')
def process_b2c_call_response_task(response, id):
    """
    process the request sent back from b2c request
    :param response:
    :param id:
    :return:
    """
    data = response
    B2CRequest.objects.filter(pk=id).update(
        request_id=data.get('requestId', ''),
        error_code=data.get('errorCode', ''),
        error_message=data.get('errorMessage', ''),
        conversation_id=data.get('ConversationID', ''),
        originator_conversation_id=data.get('OriginatorConversationID', ''),
        response_code=data.get('ResponseCode', ''),
        response_description=data.get('ResponseDescription', '')
    )


@shared_task(name='core.handle_b2c_result_response')
def process_b2c_result_response_task(response):
    """
    Process b2c result
    :param response:
    :return:
    """
    try:
        data = response.get('Result', '')
        update_data = dict()
        update_data['result_type'] = str(data.get('ResultType', ''))
        update_data['result_code'] = str(data.get('ResultCode', ''))
        update_data['result_description'] = data.get('ResultDesc', '')
        update_data['transaction_id'] = data.get('TransactionID', '')

        params = data.get('ResultParameters', {}).get('ResultParameter', {})

        if len(params) > 0:
            # means that we have data doe we handle that
            for p in params:
                key, value = p.values()

                if key == 'TransactionReceipt':
                    update_data['transaction_receipt'] = value
                elif key == 'TransactionAmount':
                    update_data['transaction_amount'] = value
                elif key == 'B2CWorkingAccountAvailableFunds':
                    update_data['working_funds'] = value
                elif key == 'B2CUtilityAccountAvailableFunds':
                    rupdate_data['utility_funds'] = value
                elif key == 'B2CChargesPaidAccountAvailableFunds':
                    update_data['paid_account_funds'] = value
                elif key == 'TransactionCompletedDateTime':
                    date, time = value.split(' ')
                    day, month, year = date.split('.')
                    trx_date = '{}-{}-{} {}'.format(year, month, day, time)
                    update_data['transaction_date'] = trx_date
                elif key == 'ReceiverPartyPublicName':
                    _, name = value.split(' - ')
                    update_data['mpesa_user_name'] = name
                elif key == 'B2CRecipientIsRegisteredCustomer':
                    update_data['is_registered_customer'] = value

        # save
        B2CRequest.objects.filter(
            originator_conversation_id=data.get('OriginatorConversationID', '')).\
            update(**update_data)
    except Exception as ex:
        pass


@shared_task(name='core.handle_c2b_validation')
def process_c2b_validation_task(response):
    """
    Handle c2b request
    {
        "TransactionType": "Pay Bill",
        "TransID": "LK631GQCSP",
        "TransTime": "20171106225323",
        "TransAmount": "100.00",
        "BusinessShortCode": "600000",
        "BillRefNumber": "Test",
        "InvoiceNumber": "",
        "OrgAccountBalance": "",
        "ThirdPartyTransID": "",
        "MSISDN": "254708374149",
        "FirstName": "John",
        "MiddleName": "J.",
        "LastName": "Doe"
    }
    :param response:
    :return:
    """
    date = response.get('TransTime', '')
    year, month, day, hour, min, sec = date[:4], date[4:-8], date[6:-6], date[8:-4], date[10:-2], date[12:]
    org_balance = 0.0
    if response.get('OrgAccountBalance', ''):
        org_balance = Decimal(response.get('OrgAccountBalance'))
    data = dict(
        transaction_type=response.get('TransactionType', ''),
        transaction_id=response.get('TransID', ''),
        transaction_date='{}-{}-{} {}:{}:{}'.format(year, month, day, hour, min, sec),
        amount=Decimal(response.get('TransAmount', '0')),
        business_short_code=response.get('BusinessShortCode', ''),
        bill_ref_number=response.get('BillRefNumber', ''),
        invoice_number=response.get('InvoiceNumber', ''),
        org_account_balance=org_balance,
        third_party_trans_id=response.get('ThirdPartyTransID', ''),
        phone=int(response.get('MSISDN', '0')),
        first_name=response.get('FirstName', ''),
        middle_name=response.get('MiddleName', ''),
        last_name=response.get('LastName', ''),
        is_validated=True
    )

    C2BRequest.objects.create(**data)


@shared_task(name='core.handle_c2b_confirmation')
def process_c2b_confirmation_task(response):
    """
    Handle c2b request
    {
        "TransactionType": "Pay Bill",
        "TransID": "LK631GQCSP",
        "TransTime": "20171106225323",
        "TransAmount": "100.00",
        "BusinessShortCode": "600000",
        "BillRefNumber": "Test",
        "InvoiceNumber": "",
        "OrgAccountBalance": "",
        "ThirdPartyTransID": "",
        "MSISDN": "254708374149",
        "FirstName": "John",
        "MiddleName": "J.",
        "LastName": "Doe"
    }
    :param response:
    :return:
    """
    date = response.get('TransTime', '')
    year, month, day, hour, min, sec = date[:4], date[4:-8], date[6:-6], date[8:-4], date[10:-2], date[12:]
    org_balance = 0.0
    if response.get('OrgAccountBalance', ''):
        org_balance = Decimal(response.get('OrgAccountBalance'))

    data = dict(
        transaction_type=response.get('TransactionType', ''),
        transaction_id=response.get('TransID', ''),
        transaction_date='{}-{}-{} {}:{}:{}'.format(year, month, day, hour, min, sec),
        amount=Decimal(response.get('TransAmount', '0')),
        business_short_code=response.get('BusinessShortCode', ''),
        bill_ref_number=response.get('BillRefNumber', ''),
        invoice_number=response.get('InvoiceNumber', ''),
        org_account_balance=org_balance,
        third_party_trans_id=response.get('ThirdPartyTransID', ''),
        phone=int(response.get('MSISDN', '0')),
        first_name=response.get('FirstName', ''),
        middle_name=response.get('MiddleName', ''),
        last_name=response.get('LastName', ''),
        is_completed=True
    )

    try:
        req = C2BRequest.objects.filter(transaction_id=response.get('TransID', ''))

        if req:
            C2BRequest.objects.filter(transaction_id=response.get('TransID', '')).update(is_completed=True)
        else:
            C2BRequest.objects.create(**data)
    except Exception as ex:
        pass
