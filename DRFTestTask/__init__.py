"""Init file for celery setup."""
from .celery import app as celery_app

__all__ = ("celery_app",)
