"""Buyer balance increase testing."""
import pytest
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Buyer
from tests.project_fixtures import buyer

c = APIClient()


@pytest.mark.django_db
def test_balance_increase(buyer):
    """Testing balance increase after user added some money."""

    user_token = c.post(
        "/api/buyer/token/",
        data={"username": buyer.account.username, "password": "TestPass123"},
    ).data["access"]
    money = 20000
    request = c.put(
        "/api/buyer/buyers/balance/",
        data={
            "card_number": "1213141516171819",
            "card_owner": "Random Name",
            "card_cvc_code": "333",
            "card_password": "1234",
            "value_of_money": money,
        },
        headers={"Authorization": f"Token {user_token}"},
    )
    assert request.status_code == status.HTTP_200_OK, "Should be equal"
    assert (
        money == Buyer.objects.values("balance").get(account=buyer.account)["balance"]
    )
