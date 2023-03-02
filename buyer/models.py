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
