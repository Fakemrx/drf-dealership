"""Module of CRUD APIViews for CarDealership model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from dealership.filters import CarDealershipFilter, CarsInStockFilter
from dealership.models import CarDealership, CarsInDealershipStock
from dealership.serializers.car_dealership_serializers import (
    CarDealershipSerializer,
    CarsInStockSerializer,
)


class CarDealershipAPIView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """APIView for list and detail view for CarDealership model."""

    queryset = CarDealership.objects.prefetch_related(
        "preferred_cars_list", "preferred_cars_list__engine"
    )
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


class CarsInStockAPIView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """APIView for list and detail view for CarsInDealershipStock model."""

    queryset = CarsInDealershipStock.objects.select_related(
        "car", "car__engine", "dealership"
    ).filter(price__gt=0, quantity__gt=0)
    serializer_class = CarsInStockSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^car"]
    ordering_fields = ["price"]
    filterset_class = CarsInStockFilter
