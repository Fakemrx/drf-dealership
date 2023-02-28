"""Custom filters for car app."""
from django_filters import rest_framework as filters

from car.models import Car, Engine


class CarFilter(filters.FilterSet):
    """Custom filtering for Car model list."""

    type_choices = (
        ("suv", "SUV"),
        ("sedan", "Sedan 4-d"),
        ("coupe", "Coupe 2-d"),
        ("sport", "Sportcar"),
        ("hyper", "Hypercar"),
        ("minivan", "Mini-van"),
        ("van", "Van"),
        ("truck", "Truck"),
        ("wagon", "Wagon"),
        ("muscle", "Musclecar"),
        ("etc", "Etc."),
    )
    release_year = filters.RangeFilter()
    car_type = filters.ChoiceFilter(choices=type_choices)
    is_active = filters.BooleanFilter()

    class Meta:
        model = Car
        fields = ["release_year", "car_type", "is_active"]


class EngineFilter(filters.FilterSet):
    """Custom filtering for Engine model list."""

    tank_choices = (
        ("gas", "Gasoline"),
        ("diesel", "Diesel"),
        ("hybrid", "Hybrid"),
        ("electro", "Electro"),
        ("etc", "Etc."),
    )
    fuel_type = filters.ChoiceFilter(choices=tank_choices)
    hp = filters.RangeFilter()
    engine_volume = filters.RangeFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = Engine
        fields = ["fuel_type", "hp", "engine_volume", "is_active"]
