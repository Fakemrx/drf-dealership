"""Provider model testing module for correct responses, correct crud operations with data."""

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from provider.models import Provider
from provider.serializers.provider_serializers import ProviderSerializer
from provider.tests.provider_app_fixtures import provider

c = APIClient()


@pytest.mark.django_db
def test_post_provider():
    """Testing POST method to add provider instance."""
    new_data = {
        "name": "Test provider",
        "foundation_year": 2022,
        "is_active": True,
    }
    request = c.post("/api/provider/providers/", new_data, format="json")
    assert request.status_code == status.HTTP_201_CREATED, "Should be 201"
    new_data["id"] = request.data["id"]
    assert new_data == request.data, "Should be equal"


@pytest.mark.django_db
def test_put_provider(provider):
    """Testing PUT method to update provider instance."""
    new_data = {
        "id": provider.id,
        "name": "Test provider updated",
        "foundation_year": 2021,
        "is_active": False,
    }
    request = c.put(f"/api/provider/providers/{provider.id}/", new_data, format="json")
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert new_data == request.data, "Should be equal"
    assert (
        new_data == ProviderSerializer(Provider.objects.get(id=provider.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_patch_provider(provider):
    """Testing PATCH method to partial update provider instance."""
    new_data = {
        "name": "Partial updated name",
    }
    expected_data = {
        "id": provider.id,
        "name": "Partial updated name",
        "foundation_year": 2000,
        "is_active": True,
    }
    request = c.patch(
        f"/api/provider/providers/{provider.id}/", new_data, format="json"
    )
    assert request.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == request.data, "Should be equal"
    assert (
        expected_data == ProviderSerializer(Provider.objects.get(id=provider.id)).data
    ), "Should be equal"


@pytest.mark.django_db
def test_delete_provider(provider):
    """Testing DELETE method to delete provider instance."""
    expected_data = {
        "id": provider.id,
        "name": "Test provider",
        "foundation_year": 2000,
        "is_active": True,
    }
    response = c.get(f"/api/provider/providers/{provider.id}/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert expected_data == response.data, "Should be equal"
    request = c.delete(f"/api/provider/providers/{provider.id}/")
    assert request.status_code == status.HTTP_204_NO_CONTENT, "Should be 204"
