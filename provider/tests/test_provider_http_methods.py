"""Provider model testing module for correct responses, correct crud operations with data."""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from provider.models import Provider
from provider.serializers.provider_serializers import ProviderSerializer
from provider.tests.provider_app_fixtures import provider

c = APIClient()


@pytest.mark.django_db
def test_get_provider(provider):
    """Testing GET method to get detailed provider instance."""
    expected_data = {
        "id": provider.id,
        "name": "Test provider",
        "foundation_year": 2000,
        "is_active": True,
    }
    request = c.get(f"/api/provider/providers/{provider.id}/")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == ProviderSerializer(Provider.objects.get(id=provider.id)).data
    ), "Should be equal"
