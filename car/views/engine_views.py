"""Module of CRUD APIViews for Engine model."""
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from django_filters.rest_framework import DjangoFilterBackend

from car.filters import EngineFilter
from car.models import Engine
from car.serializers.engine_serializers import EngineSerializer


class EngineListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    """APIView create and list-view operations for Engine model."""

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

    def post(self, request, *args, **kwargs):
        """POST method to add engine instance."""
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """GET method to get list of engine instances."""
        return self.list(request, *args, **kwargs)


class EngineRetrieveUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    """APIView retrieve, update, partial update, delete operations for Engine model."""

    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

    def get(self, request, *args, **kwargs):
        """GET method to detail engine instance."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """PUT method to update engine instance."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """PATCH method to partial update engine instance."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE method to delete engine instance."""
        return self.destroy(request, *args, **kwargs)
