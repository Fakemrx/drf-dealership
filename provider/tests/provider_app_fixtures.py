"""Fixtures for provider app"""
import pytest

from provider.models import Provider


@pytest.fixture
def provider():
    """Fixture to add provider instance."""
    provider = Provider.objects.create(
        name="Test provider", foundation_year=2000, is_active=True
    )
    return provider
