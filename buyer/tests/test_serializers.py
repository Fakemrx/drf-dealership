"""Serializers testing module to check correct adding data through them"""
import pytest

from buyer.serializers.buyer_serializers import BuyerSerializer
from buyer.serializers.offer_serializers import OfferSerializer
from tests.project_fixtures import buyer, offer, car, engine


@pytest.mark.django_db
def test_buyer_serializer(buyer):
    """Test function to check if BuyerSerializer works correctly."""
    serializer_data = BuyerSerializer(buyer).data
    expected_data = {
        "id": buyer.id,
        "account": buyer.account.id,
        "full_name": "F I O",
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
