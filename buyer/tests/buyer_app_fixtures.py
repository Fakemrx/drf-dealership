"""Fixtures for buyer app"""
import pytest
from django.contrib.auth.models import User

from buyer.models import Buyer, Offer
from car.tests.car_app_fixtures import car, engine


@pytest.fixture
def buyer():
    """Fixture to add user & buyer instance."""
    user = User.objects.create(username="TestUser", password="12344321")
    buyer = Buyer.objects.create(
        account=user,
        full_name="Full Name Str",
        age=25,
        gender="male",
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
