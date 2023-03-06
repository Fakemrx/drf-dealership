"""Offer model testing module for correct responses, correct crud operations with data."""
from decimal import Decimal

import pytest
from django.forms import model_to_dict
from rest_framework import status

from rest_framework.test import APIClient

from buyer.tests.test_serializers import offer, buyer
from car.tests.test_serializers import car, engine

c = APIClient()


@pytest.mark.django_db
def test_post_offer(buyer, car):
    """Testing POST method to add offer instance."""
    new_data = {
        "id": 1,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": "5637.00",
        "quantity": 1,
        "is_active": True,
    }
    request = c.post("/api/buyer-app/offers/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_put_offer(offer, buyer, car):
    """Testing PUT method to update offer instance."""
    new_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": "1111.00",
        "quantity": 3,
        "is_active": True,
    }
    request = c.put(f"/api/buyer-app/offers/{offer.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_patch_offer(offer, buyer, car):
    """Testing PATCH method to partial update offer instance."""
    new_data = {"max_cost": "3333.00", "is_active": False}
    expected_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": "3333.00",
        "quantity": 1,
        "is_active": False,
    }
    request = c.patch(f"/api/buyer-app/offers/{offer.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_delete_offer(offer, buyer, car):
    """Testing DELETE method to delete offer instance."""
    expected_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": "5637.00",
        "quantity": 1,
        "is_active": True,
    }
    response = c.get(f"/api/buyer-app/offers/{offer.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/buyer-app/offers/{offer.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
