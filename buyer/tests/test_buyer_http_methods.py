"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer
from tests.project_fixtures import buyer

c = APIClient()
User = get_user_model()


@pytest.mark.django_db
def test_get_buyer(buyer):
    """Testing GET method to get detailed buyer instance."""
    expected_data = {
        "id": buyer.id,
        "account": buyer.account.id,
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
        "balance": "0.00",
        "is_active": True,
    }

    db_data = Buyer.objects.get(id=buyer.id)
    assert expected_data == BuyerSerializer(db_data).data, "Should be equal"

    response = c.get(f"/api/buyer/buyers/{buyer.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"


@pytest.mark.django_db
def test_post_buyer():
    """Testing POST method to create a buyer and user instances."""
    new_data = {
        "username": "VeryUnique",
        "password": "VeryHardPass321",
        "email": "test@pytest.notio",
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
    }
    request = c.post("/api/buyer/registration/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"

    user_data = User.objects.get(username=new_data["username"], email=new_data["email"])
    buyer_data = Buyer.objects.get(
        account__username=new_data["username"], account__email=new_data["email"]
    )
    assert user_data.id == buyer_data.account.id, "Should be equal"
