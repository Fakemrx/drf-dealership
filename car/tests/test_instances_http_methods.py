"""Car app testing module for correct responses, correct crud operations with data."""
from decimal import Decimal

import pytest
from django.forms import model_to_dict

from rest_framework.test import APIClient

from car.models import Engine, Car

c = APIClient()


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


@pytest.mark.django_db
def test_post_car(engine):
    """Testing POST method to add car instance."""
    new_data = {
        "id": 1,
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    c.post("/api/car-app/cars/", new_data, format="json")
    written_data = Car.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_put_car(engine, car):
    """Testing PUT method to update car instance."""
    new_data = {
        "id": car.id,
        "car_brand": "Updated brand",
        "car_model": "Updated model",
        "release_year": 2023,
        "car_type": "sport",
        "engine": engine.id,
        "is_active": False,
    }
    c.put(f"/api/car-app/cars/{car.id}/", new_data, format="json")
    written_data = Car.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_patch_car(engine, car):
    """Testing PATCH method to partial update car instance."""
    new_data = {
        "car_brand": "Partial updated brand",
        "release_year": 2024,
    }
    expected_data = {
        "id": car.id,
        "car_brand": "Partial updated brand",
        "car_model": "Test model",
        "release_year": 2024,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    c.patch(f"/api/car-app/cars/{car.id}/", new_data, format="json")
    written_data = Car.objects.last()
    assert expected_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_delete_car(car, engine):
    """Testing DELETE method to delete car instance."""
    written_data = Car.objects.last()
    expected_data = {
        "id": car.id,
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    assert expected_data == model_to_dict(written_data), "Should be equal"
    c.delete(f"/api/car-app/cars/{car.id}/")
    written_data = Car.objects.all()
    assert written_data.exists() is False, "Should be empty"


@pytest.mark.django_db
def test_post_engine():
    """Testing POST method to add engine instance."""
    new_data = {
        "id": 5,
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": Decimal("1.5"),
        "hp": 111,
        "is_active": True,
    }
    c.post("/api/car-app/engines/", new_data, format="json")
    written_data = Engine.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_put_engine(engine):
    """Testing PUT method to update car instance."""
    new_data = {
        "id": engine.id,
        "engine_brand": "Updated Test-Brand",
        "fuel_type": "diesel",
        "engine_volume": Decimal("2.0"),
        "hp": 500,
        "is_active": True,
    }
    c.put(f"/api/car-app/engines/{engine.id}/", new_data, format="json")
    written_data = Engine.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_patch_engine(engine):
    """Testing PATCH method to partial update engine instance."""
    new_data = {"engine_brand": "Partial updated brand", "hp": 300, "is_active": False}
    expected_data = {
        "id": engine.id,
        "engine_brand": "Partial updated brand",
        "fuel_type": "gas",
        "engine_volume": Decimal("1.5"),
        "hp": 300,
        "is_active": False,
    }
    c.patch(f"/api/car-app/engines/{engine.id}/", new_data, format="json")
    written_data = Engine.objects.last()
    assert expected_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_delete_engine(engine):
    """Testing DELETE method to delete engine instance."""
    written_data = Engine.objects.last()
    expected_data = {
        "id": engine.id,
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": Decimal("1.5"),
        "hp": 111,
        "is_active": True,
    }
    assert expected_data == model_to_dict(written_data), "Should be equal"
    c.delete(f"/api/car-app/engines/{engine.id}/")
    written_data = Engine.objects.all()
    assert written_data.exists() is False, "Should be empty"
