"""Buyer tasks to buy cars from dealerships."""
from decimal import Decimal

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from buyer.models import Offer

logger = get_task_logger(__name__)


@receiver(post_save, sender=Offer)
def user_buy_car(sender, instance, created, **kwargs):
    """Celery task that buy's car according to Order information"""
    if not created:
        return "Instance was not created yet, some error occurred."
    return instance
