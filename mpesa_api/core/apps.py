from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    name = 'mpesa_api.core'
    label = 'core'
    verbose_name = 'MPESA API CORE'

    def ready(self):
        import mpesa_api.core.signals
        # from mpesa_api.core.models import B2CRequest, OnlineCheckout
        # from mpesa_api.core.signals import handle_b2c_request_post_save, \
        #     handle_online_checkout_post_save
        # post_save.connect(handle_b2c_request_post_save, sender=B2CRequest)
        # post_save.connect(handle_online_checkout_post_save, sender=OnlineCheckout)


