"""Models of Buyer app."""
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Genders(Enum):
    """Gender types choices."""

    male = "Male"
    female = "Female"


class Buyer(models.Model):
    """Model of buyer, includes full name, age, gender, balance, status (active or not)."""

    account = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, verbose_name="Full name")
    age = models.IntegerField(verbose_name="Age", default=0)
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
        return f"{self.full_name} | {self.balance} USD | {self.is_active}"


@receiver(post_save, sender=User)
def update_buyer_signal(sender, instance, created, **kwargs):
    """Signal sender to create buyer instance after user instance was created"""
    if created:
        Buyer.objects.create(account=instance)
    instance.buyer.save()


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
