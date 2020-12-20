from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'immuwallet.apps.api'

    def ready(self):
        import api.signals
