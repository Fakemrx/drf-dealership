"""Models of dealership app."""
from django.db import models
from django_countries.fields import CountryField

from car.models import CarTypes, TankTypes


class CarDealership(models.Model):
    """
    Model of car dealership, includes name, location, balance, preferred
    cars list and status (active or not).
    """

    name = models.CharField(max_length=100, verbose_name="Naming")
    location = CountryField(verbose_name="Country")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Car dealership's balance"
    )
    preferred_cars_list = models.ManyToManyField(
        "car.Car", verbose_name="List of preferred cars", null=True, blank=True
    )
    preferred_car_release_year_from = models.IntegerField(
        null=True, blank=True, verbose_name="Release year from"
    )
    preferred_car_release_year_to = models.IntegerField(
        null=True, blank=True, verbose_name="Release year to"
    )

    preferred_car_type = models.CharField(
        null=True,
        blank=True,
        choices=[(car_type.name, car_type.value) for car_type in CarTypes],
        verbose_name="Car type",
        max_length=20,
    )
    preferred_fuel_type = models.CharField(
        null=True,
        blank=True,
        choices=[(fuel_type.name, fuel_type.value) for fuel_type in TankTypes],
        verbose_name="Fuel type",
        max_length=20,
    )
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        result = f"{self.name} | {self.location} | {self.balance} | "
        if self.is_active is False:
            result += "Inactive"
        else:
            result += "Active"
        return result
