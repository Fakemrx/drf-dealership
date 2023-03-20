"""Init file for celery setup."""
from celery_tasks.celery import app as celery_app

__all__ = ("celery_app",)
