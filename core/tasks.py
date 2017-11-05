from __future__ import absolute_import, unicode_literals
from celery import shared_task
from util.b2cutils import send_b2c_request
from core.models import B2CRequest
from util.core import Map


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
