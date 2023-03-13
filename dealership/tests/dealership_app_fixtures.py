"""Fixtures for dealership app"""
import pytest

from car.models import Car, Engine
from dealership.models import CarDealership


@pytest.fixture
def dealership():
    """Fixture to add CarDealership instance."""
    dealership = CarDealership.objects.create(
        name="Test dealership",
        location="HT",
        balance=1000,
        is_active=True,
    )
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type="gas",
        engine_volume=1.5,
        hp=111,
        is_active=True,
    )
    dealership.preferred_cars_list.create(
        car_brand="Car test brand",
        car_model="Test model",
        release_year=2022,
        car_type="suv",
        engine=engine,
        is_active=True,
    )
    return dealership
