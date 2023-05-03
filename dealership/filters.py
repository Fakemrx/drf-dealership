"""Custom filters for dealership app."""
from django_countries.fields import CountryField
from django_filters import rest_framework as filters

from dealership.models import CarDealership, CarsInDealershipStock


class CarDealershipFilter(filters.FilterSet):
    """Custom filtering for CarDealership model list."""

    location = CountryField()
    balance = filters.RangeFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = CarDealership
        fields = ["location", "balance", "is_active"]


class CarsInStockFilter(filters.FilterSet):
    """Custom filtering for CarsInDealershipStock model list."""

    price = filters.RangeFilter()
    quantity = filters.RangeFilter()

    class Meta:
        model = CarsInDealershipStock
        fields = ["price", "quantity"]
