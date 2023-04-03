"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from django.contrib.auth import get_user_model
from django.db.models import F
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
        "account": {
            "username": buyer.account.username,
            "email": buyer.account.email,
            "first_name": buyer.account.first_name,
            "last_name": buyer.account.last_name,
        },
        "age": 50,
        "gender": "male",
        "balance": "0.00",
        "is_active": True,
    }

    db_data = Buyer.objects.annotate(
        username=F("account__username"),
        email=F("account__email"),
        first_name=F("account__first_name"),
        last_name=F("account__last_name"),
    ).get(id=buyer.id)
    assert expected_data == BuyerSerializer(db_data).data, "Should be equal"

    response = c.get(f"/api/buyer/buyers/{buyer.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
