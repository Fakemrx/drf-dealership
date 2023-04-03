"""Serializers testing module to check correct adding data through them"""
import pytest
from django.db.models import F

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer
from buyer.serializers.offer_serializers import OfferSerializer
from tests.project_fixtures import buyer, offer, car, engine


@pytest.mark.django_db
def test_buyer_serializer(buyer):
    """Test function to check if BuyerSerializer works correctly."""
    cur_buyer = Buyer.objects.annotate(
        username=F("account__username"),
        email=F("account__email"),
        first_name=F("account__first_name"),
        last_name=F("account__last_name"),
    ).get(account_id=buyer.account.id)
    serializer_data = BuyerSerializer(cur_buyer).data
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
    assert serializer_data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_offer_serializer(offer, car, buyer):
    """Test function to check if OfferSerializer works correctly."""
    serializer_data = OfferSerializer(offer).data
    expected_data = {
        "id": offer.id,
        "buyer": buyer.id,
        "car": car.id,
        "max_cost": "5637.00",
        "quantity": 1,
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
