"""Serializers testing module to check correct adding data through them"""
import pytest

from dealership.serializers.car_dealership_serializers import CarDealershipSerializer
from dealership.tests.dealership_app_fixtures import dealership


@pytest.mark.django_db
def test_dealership_serializer(dealership):
    """Test function to check if EngineSerializer works correctly."""
    serializer_data = CarDealershipSerializer(dealership).data
    expected_data = {
        "id": dealership.id,
        "name": "Test dealership",
        "location": "HT",
        "balance": "1000.00",
        "preferred_cars_list": [
            dealership.preferred_cars_list.values_list("id", flat=True)[0]
        ],
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
