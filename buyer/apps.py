"""
Default app settings.
"""
from django.apps import AppConfig


class BuyerConfig(AppConfig):
    """
    Default app settings class.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "buyer"
