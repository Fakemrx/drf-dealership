"""Module of CRUD APIViews for Car model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from car.filters import CarFilter
from car.models import Car
from car.serializers.car_serializers import CarSerializer


class CarAPIView(ModelViewSet):
    """APIView for CRUD operations with Car model."""

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
