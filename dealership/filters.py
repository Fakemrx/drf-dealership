"""Custom filters for dealership app."""
from django_countries.fields import CountryField
from django_filters import rest_framework as filters

# from django_countries import countries
from car.models import Car
from dealership.models import CarDealership


class CarDealershipFilter(filters.FilterSet):
    """Custom filtering for CarDealership model list."""

    location = CountryField()
    balance = filters.RangeFilter()
    is_active = filters.BooleanFilter()
    preferred_cars_list = filters.ChoiceFilter(
        choices=[(car.id, car) for car in Car.objects.all()]
    )

    class Meta:
        model = CarDealership
        fields = ["location", "balance", "preferred_cars_list", "is_active"]
