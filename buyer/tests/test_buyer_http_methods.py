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
