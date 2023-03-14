"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer
from tests.project_fixtures import buyer

c = APIClient()


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
    """Testing POST method to create buyer instance."""
    new_data = {
        "username": "VeryUnique",
        "password1": "VeryHardPass321",
        "password2": "VeryHardPass321",
        "email": "test@pytest.notio",
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
    }
    request = c.post("/api/buyer/reg/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"

    # user_data = User.objects.get(username="TestUserName", email="test@pytest.notio")
    # buyer_data = Buyer.objects.get(account__username="TestUserName",
    #                                account__email="test@pytest.notio")
    # assert 8 == buyer_data.account.id, "Should be equal"
    # Никита, каким более нормальным образом я могу еще проверить то, что запись создалась
    # правильно? Мне надо посмотреть, что в User создалась запись и в Buyer
    # создалась запись, а самое главное - проверить то, что они связались правильно
