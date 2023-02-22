"""
Default app settings.
"""
from django.apps import AppConfig


class CarConfig(AppConfig):
    """
    Default app settings class.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "car"
