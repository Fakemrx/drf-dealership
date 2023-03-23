"""Celery setup."""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRFTestTask.settings")
app = Celery("DRFTestTask")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
