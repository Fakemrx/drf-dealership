"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from django.forms import model_to_dict

from rest_framework.test import APIClient

from buyer.models import Buyer

c = APIClient()


@pytest.fixture
def buyer():
    """Fixture to add buyer instance."""
    buyer = Buyer.objects.create(
        full_name="F I O",
        age=50,
        gender="male",
        balance=1111,
        is_active=True,
    )
    return buyer


@pytest.mark.django_db
def test_post_buyer():
    """Testing POST method to add buyer instance."""
    new_data = {
        "id": 1,
        "full_name": "F I O",
        "age": 53,
        "gender": "male",
        "balance": 1000,
        "is_active": True,
    }
    c.post("/api/buyer-app/buyers/", new_data, format="json")
    written_data = Buyer.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_put__buyer(buyer):
    """Testing PUT method to update buyer instance."""
    new_data = {
        "id": buyer.id,
        "full_name": "F I O",
        "age": 53,
        "gender": "male",
        "balance": 1000,
        "is_active": True,
    }
    c.put(f"/api/buyer-app/buyers/{buyer.id}/", new_data, format="json")
    written_data = Buyer.objects.last()
    assert new_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_patch_buyer(buyer):
    """Testing PATCH method to partial update buyer instance."""
    new_data = {"full_name": "FI O O", "balance": 1500}
    expected_data = {
        "id": buyer.id,
        "full_name": "FI O O",
        "age": 50,
        "gender": "male",
        "balance": 1500,
        "is_active": True,
    }
    c.patch(f"/api/buyer-app/buyers/{buyer.id}/", new_data, format="json")
    written_data = Buyer.objects.last()
    assert expected_data == model_to_dict(written_data), "Should be equal"


@pytest.mark.django_db
def test_delete_buyer(buyer):
    """Testing DELETE method to delete buyer instance."""
    written_data = Buyer.objects.last()
    expected_data = {
        "id": buyer.id,
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
        "balance": 1111,
        "is_active": True,
    }
    assert expected_data == model_to_dict(written_data), "Should be equal"
    c.delete(f"/api/buyer-app/buyers/{buyer.id}/")
    written_data = Buyer.objects.all()
    assert written_data.exists() is False, "Should be empty"
