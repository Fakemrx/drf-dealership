"""Celery tasks for provider's models."""
import json
import random

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Avg

logger = get_task_logger(__name__)


@shared_task
def create_provider():
    """
    Celery task, creates a provider using
    data from providers.json.
    """

    json_path = "data_for_celery_tasks/providers.json"
    with open(json_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    random_entry = random.choice(data)
    check_and_create_provider(random_entry)


def check_and_create_provider(random_entry):
    """Check if same provider already exists, if not - add as new."""
    from provider.models import Provider

    if not Provider.objects.filter(
        name=random_entry["name"],
        foundation_year=random_entry["foundation_year"],
    ).exists():
        provider = Provider.objects.create(
            name=random_entry["name"],
            foundation_year=random_entry["foundation_year"],
            is_active=True,
        )
        logger.info(f"Created provider {provider}")


@shared_task
def add_car_to_provider_stock():
    """
    Celery task, creates a new entry in provider's stock.
    """
    from provider.models import Provider
    from car.models import Car

    cars_id = list(Car.objects.values_list("id"))
    providers_id = list(Provider.objects.values_list("id"))
    if len(providers_id) > 1 and len(cars_id) > 1:
        random_provider_id = random.choice(providers_id)[0]
        random_car_id = random.choice(cars_id)[0]
        random_provider = Provider.objects.get(id=random_provider_id)
        random_car = Car.objects.get(id=random_car_id)
        create_provider_stock(random_provider, random_car)


def create_provider_stock(random_provider, random_car):
    """Add a car in a current provider's stock if it does not exist."""
    from provider.models import CarsInProviderStock

    if not CarsInProviderStock.objects.filter(
        provider=random_provider,
        car=random_car,
    ).exists():
        if CarsInProviderStock.objects.filter(car=random_car).exists():
            average_price = CarsInProviderStock.objects.filter(
                car=random_car
            ).aggregate(avg_value=Avg("price"))["avg_value"]
        else:
            average_price = random.randint(5000, 100000)
        average_price += random.randint(-3000, +3000)
        provider_stock = CarsInProviderStock.objects.create(
            provider=random_provider, car=random_car, price=average_price
        )
        logger.info(f"Added car to provider stock: {provider_stock}")
