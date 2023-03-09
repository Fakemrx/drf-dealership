"""
CarDealership model testing module for correct responses,
correct crud operations with data.
"""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from dealership.models import CarDealership
from dealership.serializers.car_dealership_serializers import CarDealershipSerializer
from dealership.tests.dealership_app_fixtures import dealership

c = APIClient()


@pytest.mark.django_db
def test_post_dealership():
    """Testing POST method to add dealership instance."""
    new_data = {
        "name": "Dealership test name",
        "location": "HT",
        "balance": "1001.11",
        "is_active": False,
    }
    request = c.post("/api/dealer/dealerships/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    new_data["id"] = request.data["id"]
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_put_dealership(dealership):
    """Testing PUT method to update dealership instance."""
    new_data = {
        "id": dealership.id,
        "name": "Dealership updated name",
        "location": "GF",
        "balance": "2001.11",
        "is_active": False,
    }
    request = c.put(
        f"/api/dealer/dealerships/{dealership.id}/", new_data, format="json"
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert (
        new_data
        == CarDealershipSerializer(CarDealership.objects.get(id=dealership.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_patch_dealership(dealership):
    """Testing PATCH method to partial update dealership instance."""
    new_data = {
        "name": "Partial updated name",
        "balance": "5111.00",
    }
    expected_data = {
        "id": dealership.id,
        "name": "Partial updated name",
        "location": "HT",
        "balance": "5111.00",
        "is_active": True,
    }
    request = c.patch(
        f"/api/dealer/dealerships/{dealership.id}/", new_data, format="json"
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data
        == CarDealershipSerializer(CarDealership.objects.get(id=dealership.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_dealership(dealership):
    """Testing DELETE method to delete dealership instance."""
    expected_data = {
        "id": dealership.id,
        "name": "Test dealership",
        "location": "HT",
        "balance": "1000.00",
        "is_active": True,
    }
    response = c.get(f"/api/dealer/dealerships/{dealership.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/dealer/dealerships/{dealership.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
