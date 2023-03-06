"""Offer model testing module for correct responses, correct crud operations with data."""
from decimal import Decimal

import pytest
from django.forms import model_to_dict

from rest_framework.test import APIClient

from buyer.models import Offer
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
        "max_cost": Decimal("5637.00"),
        "quantity": 1,
        "is_active": True,
    }
    c.post("/api/buyer-app/offers/", new_data, format="json")
    written_data = Offer.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_put_offer(offer, buyer, car):
    """Testing PUT method to update offer instance."""
    new_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": Decimal("1111.00"),
        "quantity": 3,
        "is_active": True,
    }
    c.put(f"/api/buyer-app/offers/{offer.id}/", new_data, format="json")
    written_data = Offer.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_patch_offer(offer, buyer, car):
    """Testing PATCH method to partial update offer instance."""
    new_data = {"max_cost": "3333.00", "is_active": False}
    expected_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": Decimal("3333.00"),
        "quantity": 1,
        "is_active": False,
    }
    c.patch(f"/api/buyer-app/offers/{offer.id}/", new_data, format="json")
    written_data = Offer.objects.last()
    assert expected_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_delete_offer(offer, buyer, car):
    """Testing DELETE method to delete offer instance."""
    written_data = Offer.objects.last()
    expected_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": Decimal("5637.00"),
        "quantity": 1,
        "is_active": True,
    }
    assert expected_data == model_to_dict(written_data), "Should be equal"
    c.delete(f"/api/buyer-app/offers/{offer.id}/")
    written_data = Offer.objects.all()
    assert written_data.exists() is False, "Should be empty"
