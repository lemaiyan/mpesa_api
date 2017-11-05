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
