"""Module of CRUD APIViews for Provider model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from provider.filters import ProviderFilter
from provider.models import Provider
from provider.serializers.provider_serializers import ProviderSerializer


class ProviderAPIView(ModelViewSet):
    """APIView for CRUD operations with Provider model."""

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^name"]
    ordering_fields = ["name", "foundation_year"]
    ordering = ["name"]
    filterset_class = ProviderFilter
