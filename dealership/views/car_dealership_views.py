"""Module of CRUD APIViews for CarDealership model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from dealership.filters import CarDealershipFilter
from dealership.models import CarDealership
from dealership.serializers.car_dealership_serializers import CarDealershipSerializer


class CarDealershipAPIView(ModelViewSet):
    """APIView for CRUD operations with CarDealership model."""

    queryset = CarDealership.objects.all()
    serializer_class = CarDealershipSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^name"]
    ordering_fields = ["balance", "name"]
    ordering = ["name"]
    filterset_class = CarDealershipFilter
