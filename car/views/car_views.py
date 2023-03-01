"""Module of CRUD APIViews for Car model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)

from car.filters import CarFilter
from car.models import Car
from car.serializers.car_serializers import CarSerializer


class CarListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    """APIView create and list-view operations for Car model."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^car_brand", "^car_model"]
    ordering_fields = ["release_year", "car_brand"]
    ordering = ["car_brand"]
    filterset_class = CarFilter

    def post(self, request, *args, **kwargs):
        """POST method to add car instance."""
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """GET method to get list of car instances."""
        return self.list(request, *args, **kwargs)


class CarRetrieveUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    """APIView retrieve, update, delete operations for Car model."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get(self, request, *args, **kwargs):
        """GET method to detail car instance."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """PUT method to update car instance."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """PATCH method to partial update car instance."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE method to delete car instance."""
        return self.destroy(request, *args, **kwargs)
