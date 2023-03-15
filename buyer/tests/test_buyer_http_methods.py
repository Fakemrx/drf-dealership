"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer
from tests.project_fixtures import buyer

c = APIClient()


@pytest.mark.django_db
def test_post_buyer():
    """Testing POST method to add buyer instance."""
    new_data = {
        "id": 1,
        "full_name": "F I O",
        "age": 53,
        "gender": "male",
        "balance": "1000.00",
        "is_active": True,
    }
    request = c.post("/api/buyer/buyers/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_put_buyer(buyer):
    """Testing PUT method to update buyer instance."""
    new_data = {
        "id": buyer.id,
        "full_name": "F I O",
        "age": 53,
        "gender": "male",
        "balance": "1000.00",
        "is_active": True,
    }
    request = c.put(f"/api/buyer/buyers/{buyer.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert (
        new_data == BuyerSerializer(Buyer.objects.get(id=buyer.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_patch_buyer(buyer):
    """Testing PATCH method to partial update buyer instance."""
    new_data = {"full_name": "FI O O", "balance": "1500.00"}
    expected_data = {
        "id": buyer.id,
        "full_name": "FI O O",
        "age": 50,
        "gender": "male",
        "balance": "1500.00",
        "is_active": True,
    }
    request = c.patch(f"/api/buyer/buyers/{buyer.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == BuyerSerializer(Buyer.objects.get(id=buyer.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_buyer(buyer):
    """Testing DELETE method to delete buyer instance."""
    expected_data = {
        "id": buyer.id,
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
        "balance": "1111.00",
        "is_active": True,
    }
    response = c.get(f"/api/buyer/buyers/{buyer.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/buyer/buyers/{buyer.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
