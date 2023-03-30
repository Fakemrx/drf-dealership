"""Celery tasks for cars, engines."""
import json
import random

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def create_engine():
    """
    Celery task, creates a bunch of engines using
    data from engines.json.
    """

    json_path = "data_for_celery_tasks/engines.json"
    with open(json_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    random_entry = random.choice(data)
    check_and_create_engine(random_entry)


def check_and_create_engine(random_entry):
    """Check if same engine already exists, if not - add as new."""
    from car.models import Engine

    if not Engine.objects.filter(
        engine_brand=random_entry["engine_brand"],
        engine_volume=random_entry["engine_volume"],
        fuel_type=random_entry["fuel_type"],
        hp=random_entry["hp"],
    ).exists():
        Engine.objects.create(
            engine_brand=random_entry["engine_brand"],
            engine_volume=random_entry["engine_volume"],
            fuel_type=random_entry["fuel_type"],
            hp=random_entry["hp"],
        )


@shared_task
def create_car():
    """
    Celery task, creates a bunch of cars using
    data from cars.json.
    """

    json_path = "data_for_celery_tasks/cars.json"
    with open(json_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    random_entry = random.choice(data)
    check_and_create_car(random_entry)


def check_and_create_car(random_entry):
    """Check if same car already exists, if not - add as new."""
    from car.models import Car
    from car.models import Engine

    engines_quantity = Engine.objects.count()
    if engines_quantity > 1:
        random_id = random.randint(1, Engine.objects.count())
        random_engine = Engine.objects.get(id=random_id)
        if not Car.objects.filter(
            car_brand=random_entry["car_brand"],
            car_model=random_entry["car_model"],
            release_year=random_entry["release_year"],
            car_type=random_entry["car_type"],
            engine=random_engine,
        ).exists():
            Car.objects.create(
                car_brand=random_entry["car_brand"],
                car_model=random_entry["car_model"],
                release_year=random_entry["release_year"],
                car_type=random_entry["car_type"],
                engine=random_engine,
            )
