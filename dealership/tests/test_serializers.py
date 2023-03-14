"""Serializers testing module to check correct adding data through them"""
import pytest

from dealership.serializers.car_dealership_serializers import CarDealershipSerializer
from tests.project_fixtures import dealership


@pytest.mark.django_db
def test_dealership_serializer(dealership):
    """Test function to check if DealershipSerializer works correctly."""
    serializer_data = CarDealershipSerializer(dealership).data
    expected_data = {
        "id": dealership.id,
        "name": "Test dealer",
        "location": "HT",
        "balance": "2000.00",
        "preferred_cars_list": [],
        "preferred_car_release_year_from": 2010,
        "preferred_car_release_year_to": 2015,
        "preferred_car_type": "sedan",
        "preferred_fuel_type": "gas",
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
