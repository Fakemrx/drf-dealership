"""Fixtures for buyer app"""
import pytest

from buyer.models import Buyer, Offer
from car.tests.car_app_fixtures import car, engine


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
