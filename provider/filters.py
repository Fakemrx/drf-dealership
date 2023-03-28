"""Custom filters for provider app."""
from django_filters import rest_framework as filters

from provider.models import Provider


class ProviderFilter(filters.FilterSet):
    """Custom filtering for Provider model list."""

    foundation_year = filters.RangeFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = Provider
        fields = ["foundation_year", "is_active"]
