"""Serializers testing module to check correct adding data through them"""
import pytest

from buyer.models import Buyer, Offer
from buyer.serializers.buyer_serializers import BuyerSerializer
from buyer.serializers.offer_serializers import OfferSerializer
from car.tests.test_serializers import car, engine


@pytest.fixture
def buyer():
    """Fixture to add buyer instance."""
    buyer = Buyer.objects.create(
        full_name="F I O",
        age=50,
        gender="male",
        balance=1111,
        is_active=True,
    )
    return buyer


@pytest.fixture
def offer(car, buyer):
    """Fixture to add offer instance."""
    offer = Offer.objects.create(
        buyer=buyer,
        car=car,
        max_cost=5637,
        quantity=1,
        is_active=True,
    )
    return offer


@pytest.mark.django_db
def test_buyer_serializer(buyer):
    """Test function to check if BuyerSerializer works correctly."""
    serializer_data = BuyerSerializer(buyer).data
    expected_data = {
        "id": buyer.id,
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
        "balance": "1111.00",
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
