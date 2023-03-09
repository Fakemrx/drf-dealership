"""Fixtures for car app"""
import pytest

from car.models import Engine, Car


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
