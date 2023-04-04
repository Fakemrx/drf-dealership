"""Buyer model testing module for correct registration."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from buyer.models import Buyer

c = APIClient()
User = get_user_model()


@pytest.mark.django_db
def test_post_buyer():
    """Testing POST method to create a buyer and user instances."""
    new_data = {
        "username": "VeryUnique",
        "password": "VeryHardPass321",
        "email": "test@pytest.notio",
        "first_name": "Abraham",
        "last_name": "Lincoln",
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
