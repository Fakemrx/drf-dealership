"""
CarDealership model testing module for correct responses,
correct crud operations with data.
"""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from dealership.models import CarDealership
from dealership.serializers.car_dealership_serializers import CarDealershipSerializer
from dealership.tests.dealership_app_fixtures import dealership

c = APIClient()


@pytest.mark.django_db
def test_get_dealership(dealership):
    """Testing GET method to get detailed dealership instance."""
    expected_data = {
        "id": dealership.id,
        "name": "Test dealership",
        "location": "HT",
        "balance": "1000.00",
        "is_active": False,
    }
    request = c.get(f"/api/dealer/dealerships/{dealership.id}/")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data
        == CarDealershipSerializer(CarDealership.objects.get(id=dealership.id)).data
    ), "Should be equal"
