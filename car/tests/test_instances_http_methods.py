"""Car app testing module for correct responses, correct crud operations with data."""
import pytest

from rest_framework import status
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
    c.post("/api/cars/", new_data, format="json")
    expected_data = new_data
    response = c.get("/api/cars/1/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_put_car(engine, car):
    """Testing PUT method to update car instance."""
    new_data = {
        "id": 2,
        "car_brand": "Updated brand",
        "car_model": "Updated model",
        "release_year": 2023,
        "car_type": "sport",
        "engine": engine.id,
        "is_active": False,
    }
    c.put("/api/cars/2/", new_data, format="json")
    response = c.get("/api/cars/2/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == new_data, "Should be equal"


@pytest.mark.django_db
def test_patch_car(engine, car):
    """Testing PATCH method to partial update car instance."""
    new_data = {
        "car_brand": "Partial updated brand",
        "release_year": 2024,
    }
    expected_data = {
        "id": 3,
        "car_brand": "Partial updated brand",
        "car_model": "Test model",
        "release_year": 2024,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    c.patch("/api/cars/3/", new_data, format="json")
    response = c.get("/api/cars/3/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_delete_car(car):
    """Testing DELETE method to delete car instance."""
    response = c.get("/api/cars/4/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    c.delete("/api/cars/4/")
    response = c.get("/api/cars/4/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, "Should be 404"


@pytest.mark.django_db
def test_post_engine():
    """Testing POST method to add engine instance."""
    new_data = {
        "id": 5,
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 111,
        "is_active": True,
    }
    c.post("/api/cars/engines/", new_data, format="json")
    expected_data = new_data
    response = c.get("/api/cars/engines/5/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_put_engine(engine):
    """Testing PUT method to update car instance."""
    new_data = {
        "id": 6,
        "engine_brand": "Updated Test-Brand",
        "fuel_type": "diesel",
        "engine_volume": "2.0",
        "hp": 500,
        "is_active": True,
    }
    c.put("/api/cars/engines/6/", new_data, format="json")
    response = c.get("/api/cars/engines/6/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == new_data, "Should be equal"


@pytest.mark.django_db
def test_patch_engine(engine):
    """Testing PATCH method to partial update engine instance."""
    new_data = {"engine_brand": "Partial updated brand", "hp": 300, "is_active": False}
    expected_data = {
        "id": 7,
        "engine_brand": "Partial updated brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 300,
        "is_active": False,
    }
    c.patch("/api/cars/engines/7/", new_data, format="json")
    response = c.get("/api/cars/engines/7/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_delete_engine(engine):
    """Testing DELETE method to delete engine instance."""
    response = c.get("/api/cars/engines/8/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    request = c.delete("/api/cars/engines/8/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
    response = c.get("/api/cars/engines/8/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, "Should be 404"
