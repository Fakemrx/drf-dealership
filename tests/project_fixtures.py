"""Fixtures for all project tests"""
import pytest
from django.contrib.auth.models import User

from car.models import Engine, Car
from buyer.models import Buyer, Offer


@pytest.fixture
def engine():
    """Fixture to add engine instance."""
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type="gas",
        engine_volume=1.5,
        hp=111,
        is_active=True,
    )
    return engine


@pytest.fixture
def car(engine):
    """Fixture to add car instance."""
    car = Car.objects.create(
        car_brand="Car test brand",
        car_model="Test model",
        release_year=2022,
        car_type="suv",
        engine=engine,
        is_active=True,
    )
    return car


@pytest.fixture
def buyer():
    """Fixture to add buyer instance."""
    user = User.objects.create_user(
        username="TestUsr",
        password="TestPass123",
        email="test@pytest.io",
    )
    buyer = Buyer.objects.get(account=user)
    buyer.full_name = "F I O"
    buyer.age = 50
    buyer.gender = "male"
    buyer.save()
    return buyer


@pytest.fixture
def offer(car, buyer):
    """Fixture to add offer instance."""
    offer = Offer.objects.create(
        buyer=buyer,
        car=car,
        max_cost=5637,
        quantity=1,
        is_active=True,
    )
    return offer
