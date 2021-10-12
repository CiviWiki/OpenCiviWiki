from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # flake8: noqa: F401
    def ready(self):
        import accounts.signals
