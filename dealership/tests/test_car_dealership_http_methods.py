"""
CarDealership model testing module for correct responses,
correct crud operations with data.
"""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from dealership.models import CarDealership
from dealership.serializers.car_dealership_serializers import CarDealershipSerializer
from tests.project_fixtures import dealership, car, engine

c = APIClient()


@pytest.mark.django_db
def test_get_dealership(dealership):
    """Testing GET method to get detailed dealership instance."""
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
    request = c.get(f"/api/dealer/dealerships/{dealership.id}/")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data
        == CarDealershipSerializer(CarDealership.objects.get(id=dealership.id)).data
    ), "Should be equal"
