"""Custom filters for car app."""
from django_filters import rest_framework as filters

from car.models import Car, Engine, CarTypes, TankTypes


class CarFilter(filters.FilterSet):
    """Custom filtering for Car model list."""

    release_year = filters.RangeFilter()
    car_type = filters.ChoiceFilter(
        choices=[(car_type.name, car_type.value) for car_type in CarTypes]
    )
    is_active = filters.BooleanFilter()

    class Meta:
        model = Car
        fields = ["release_year", "car_type", "is_active"]


class EngineFilter(filters.FilterSet):
    """Custom filtering for Engine model list."""

    fuel_type = filters.ChoiceFilter(
        choices=[(tank.name, tank.value) for tank in TankTypes]
    )
    hp = filters.RangeFilter()
    engine_volume = filters.RangeFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = Engine
        fields = ["fuel_type", "hp", "engine_volume", "is_active"]
