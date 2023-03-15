"""Fixtures for all project tests"""
import pytest
from django.contrib.auth import get_user_model

from car.models import Engine, Car
from buyer.models import Buyer, Offer
from dealership.models import CarDealership

User = get_user_model()


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
    buyer = Buyer.objects.create(
        account=user,
        full_name="F I O",
        age=50,
        gender="male",
    )
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


@pytest.fixture
def dealership():
    """Fixture to add CarDealership instance."""
    dealership = CarDealership.objects.create(
        name="Test dealer",
        location="HT",
        balance=2000.00,
        preferred_car_release_year_from=2010,
        preferred_car_release_year_to=2015,
        preferred_car_type="sedan",
        preferred_fuel_type="gas",
        is_active=True,
    )
    return dealership
