"""Fixtures for dealership app"""
import pytest

from dealership.models import CarDealership


@pytest.fixture
def dealership():
    """Fixture to add CarDealership instance."""
    dealership = CarDealership.objects.create(
        name="Test dealership",
        location="HT",
        balance=1000,
        is_active=True,
    )
    return dealership
