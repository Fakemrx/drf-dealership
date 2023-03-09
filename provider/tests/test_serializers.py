"""Serializers testing module to check correct adding data through them"""
import pytest

from provider.serializers.provider_serializers import ProviderSerializer
from provider.tests.provider_app_fixtures import provider


@pytest.mark.django_db
def test_provider_serializer(provider):
    """Test function to check if ProviderSerializer works correctly."""
    serializer_data = ProviderSerializer(provider).data
    expected_data = {
        "id": provider.id,
        "name": "Test provider",
        "foundation_year": 2000,
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
