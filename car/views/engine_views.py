"""Module of CRUD APIViews for Engine model."""
from rest_framework import filters
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from car.filters import EngineFilter
from car.models import Engine
from car.serializers.engine_serializers import EngineSerializer


class EngineAPIView(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    """APIView for CRUD operations with Engine model."""

    queryset = Engine.objects.all()
    serializer_class = EngineSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^engine_brand"]
    ordering_fields = ["hp", "engine_volume", "engine_brand"]
    ordering = ["engine_brand"]
    filterset_class = EngineFilter
