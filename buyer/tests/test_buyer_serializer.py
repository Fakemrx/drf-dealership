"""Serializers testing module to check correct adding data through them"""
import pytest

from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer


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


@pytest.mark.django_db
def test_buyer_serializer(buyer):
    """Test function to check if BuyerSerializer works correctly."""
    serializer_data = BuyerSerializer(buyer).data
    expected_data = {
        "id": 5,
        "full_name": "F I O",
        "age": 50,
        "gender": "male",
        "balance": "1111.00",
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
