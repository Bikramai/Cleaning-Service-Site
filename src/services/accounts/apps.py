from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'src.services.accounts'
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    default_auto_config = 'django.db.models.BigAutoField'

    def ready(self):
        import src.services.accounts.signals
