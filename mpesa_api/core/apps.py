from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'mpesa_api.core'

    def ready(self):
        pass
