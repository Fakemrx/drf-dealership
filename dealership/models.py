"""Models of dealership app."""
from django.db import models
from django_countries.fields import CountryField


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
        "car.Car", verbose_name="List of preferred cars"
    )
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        result = f"{self.name} | {self.location} | {self.balance} | "
        if self.is_active is False:
            result += "Inactive"
        else:
            result += "Active"
        return result
