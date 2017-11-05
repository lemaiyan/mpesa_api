from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import B2CRequest
from core.tasks import send_b2c_request_task, process_b2c_call_response_task
from celery import chain


@receiver(post_save, sender=B2CRequest)
def handle_b2c_request_post_save(sender, instance, **kwargs):
    """
    Handles B2CRequest post_save
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """

    # call the mpesa
    chain(send_b2c_request_task.s(int(instance.amount), instance.phone, instance.id),
          process_b2c_call_response_task.s(instance.id)).apply_async(queue='b2c_request')
