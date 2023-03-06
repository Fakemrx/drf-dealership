"""Models of Buyer app."""
from django.db import models


class Buyer(models.Model):
    """Model of buyer, includes full name, age, gender, balance, status (active or not)."""

    GENDER_CHOICES = (("male", "Male"), ("female", "Female"))
    full_name = models.CharField(max_length=100, verbose_name="Full name")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, verbose_name="Gender"
    )
    balance = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Buyer's balance"
    )
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        return f"{self.full_name} | {self.balance} USD | {self.is_active}"


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
            f"{self.buyer.full_name} want to buy {self.quantity} {self.car}, max price "
            f"per 1 vehicle - {self.max_cost} USD"
        )
