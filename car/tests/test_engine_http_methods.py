"""Engine model testing module for correct responses, correct crud operations with data."""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from car.models import Engine
from car.serializers.engine_serializers import EngineSerializer
from tests.project_fixtures import engine

c = APIClient()


@pytest.mark.django_db
def test_post_engine():
    """Testing POST method to add engine instance."""
    new_data = {
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 111,
        "is_active": True,
    }
    request = c.post("/api/car/engines/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    new_data["id"] = request.data["id"]
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_put_engine(engine):
    """Testing PUT method to update car instance."""
    new_data = {
        "id": engine.id,
        "engine_brand": "Updated Test-Brand",
        "fuel_type": "diesel",
        "engine_volume": "2.0",
        "hp": 500,
        "is_active": True,
    }
    request = c.put(f"/api/car/engines/{engine.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert (
        new_data == EngineSerializer(Engine.objects.get(id=engine.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_patch_engine(engine):
    """Testing PATCH method to partial update engine instance."""
    new_data = {"engine_brand": "Partial updated brand", "hp": 300, "is_active": False}
    expected_data = {
        "id": engine.id,
        "engine_brand": "Partial updated brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 300,
        "is_active": False,
    }
    request = c.patch(f"/api/car/engines/{engine.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == EngineSerializer(Engine.objects.get(id=engine.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_engine(engine):
    """Testing DELETE method to delete engine instance."""
    expected_data = {
        "id": engine.id,
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 111,
        "is_active": True,
    }
    response = c.get(f"/api/car/engines/{engine.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/car/engines/{engine.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
