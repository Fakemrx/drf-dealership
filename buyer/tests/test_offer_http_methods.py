"""Offer model testing module for correct responses, correct crud operations with data."""
import pytest
from rest_framework import status

from rest_framework.test import APIClient

from buyer.models import Offer
from buyer.serializers.offer_serializers import OfferSerializer
from buyer.tests.test_balance_changer import test_balance_increase
from tests.get_token import get_user_token
from tests.project_fixtures import offer, buyer, car, engine

c = APIClient()


@pytest.mark.django_db
def test_post_offer(buyer, car):
    """Testing POST method to add offer instance."""
    test_balance_increase(buyer)
    new_data = {
        "car": car.id,
        "max_cost": "5637.00",
    }
    request = c.post(
        "/api/buyer/offers/",
        data=new_data,
        format="json",
        headers={"Authorization": f"Token {get_user_token(buyer)}"},
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    expected_data = {
        "id": request.data["message"]["id"],
        "buyer": str(buyer),
        "car": car.id,
        "max_cost": "5637.00",
    }
    assert expected_data == request.data["message"], "Should be equal"


@pytest.mark.django_db
def test_put_offer(offer, buyer, car):
    """Testing PUT method to update offer instance."""
    test_balance_increase(buyer)
    new_data = {
        "id": offer.id,
        "buyer": str(buyer),
        "car": car.id,
        "max_cost": "1111.00",
    }
    token = get_user_token(buyer)
    request = c.put(
        f"/api/buyer/offers/{offer.id}/",
        new_data,
        format="json",
        headers={"Authorization": f"Token {token}"},
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert (
        new_data == OfferSerializer(Offer.objects.get(id=offer.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_patch_offer(offer, buyer, car):
    """Testing PATCH method to partial update offer instance."""
    test_balance_increase(buyer)
    new_data = {"max_cost": "3333.00"}
    expected_data = {
        "id": offer.id,
        "buyer": str(buyer),
        "car": car.id,
        "max_cost": "3333.00",
    }
    token = get_user_token(buyer)
    request = c.patch(
        f"/api/buyer/offers/{offer.id}/",
        new_data,
        format="json",
        headers={"Authorization": f"Token {token}"},
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == OfferSerializer(Offer.objects.get(id=offer.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_offer(offer, buyer, car):
    """Testing DELETE method to delete offer instance."""
    expected_data = {
        "id": offer.id,
        "buyer": str(buyer),
        "car": car.id,
        "max_cost": "5637.00",
    }
    token = get_user_token(buyer)
    response = c.get(
        f"/api/buyer/offers/{offer.id}/", headers={"Authorization": f"Token {token}"}
    )
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(
        f"/api/buyer/offers/{offer.id}/", headers={"Authorization": f"Token {token}"}
    )
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
