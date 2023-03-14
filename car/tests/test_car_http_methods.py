"""Car model testing module for correct responses, correct crud operations with data."""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from car.models import Car
from car.serializers.car_serializers import CarSerializer
from tests.project_fixtures import car, engine

c = APIClient()


@pytest.mark.django_db
def test_post_car(engine):
    """Testing POST method to add car instance."""
    new_data = {
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    request = c.post("/api/car/cars/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    new_data["id"] = request.data["id"]
    assert new_data == request.data, "Should be equal"


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
    request = c.put(f"/api/car/cars/{car.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert new_data == CarSerializer(Car.objects.get(id=car.id)).data, "Should be equal"


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
    request = c.patch(f"/api/car/cars/{car.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == CarSerializer(Car.objects.get(id=car.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_car(car, engine):
    """Testing DELETE method to delete car instance."""
    expected_data = {
        "id": car.id,
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    response = c.get(f"/api/car/cars/{car.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/car/cars/{car.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
