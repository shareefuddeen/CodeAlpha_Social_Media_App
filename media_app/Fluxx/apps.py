from django.apps import AppConfig


class FluxxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Fluxx"


def ready(self):
    import Fluxx.signals