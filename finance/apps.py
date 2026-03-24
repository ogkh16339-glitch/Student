from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'
from django.apps import AppConfig

class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'

    def ready(self):
        import finance.signals  # Signalni shu yerda chaqiramiz