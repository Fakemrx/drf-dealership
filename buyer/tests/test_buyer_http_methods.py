"""Buyer model testing module for correct responses, crud operations with data."""
import pytest
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer
from buyer.tests.buyer_app_fixtures import buyer

c = APIClient()

# @pytest.mark.django_db
# def test_get_buyer(buyer):
#     """Testing GET method to get detailed buyer instance."""
#     new_data = {
#         "id": buyer.id,
#         "account": buyer.account,
#         "full_name": "Full Name Str",
#         "age": 25,
#         "gender": "male",
#         "balance": "0.00",
#         "is_active": True,
#     }
#     request = c.get(f"/api/buyer/buyers/{buyer.id}", new_data, format="json")
#     assert request.status_code == status.HTTP_200_OK, "Should be 200"
#     assert new_data == request.data, "Should be equal"
