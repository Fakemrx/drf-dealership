"""Models of Buyer app."""
from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genders(Enum):
    """Gender types choices."""

    male = "Male"
    female = "Female"


class Buyer(models.Model):
    """Model of buyer, includes full name, age, gender, balance, status (active or not)."""

    account = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(
        max_length=20,
        choices=[(gender.name, gender.value) for gender in Genders],
        verbose_name="Gender",
    )
    balance = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Buyer's balance", default=0
    )
    is_active = models.BooleanField(verbose_name="Is active", default=True)

    def __str__(self):
        return (
            f"{self.account.first_name} {self.account.last_name} | "
            f"{self.balance} USD | {self.is_active}"
        )


class Offer(models.Model):
    """
    Model of offer, includes buyer field referenced to Buyer model, car referenced to Car
    model in Car app, maximum cost which buyer can pay per each vehicle, quantity of vehicles.
    """

    buyer = models.ForeignKey(
        "buyer.Buyer", on_delete=models.CASCADE, verbose_name="Buyer"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    max_cost = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Maximum cost"
    )
    quantity = models.IntegerField(verbose_name="Quantity of cars")
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        return (
            f"{self.buyer.account.first_name} {self.buyer.account.last_name} "
            f"want to buy {self.quantity} {self.car}, max price "
            f"per 1 vehicle - {self.max_cost} USD"
        )
