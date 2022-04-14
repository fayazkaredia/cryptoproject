from django.apps import AppConfig


class CryptostoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptostore'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals