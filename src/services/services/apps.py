from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.services.services'
    verbose_name = 'Service'
    verbose_name_plural = 'Services'

    def ready(self):
        import src.services.services.signals
