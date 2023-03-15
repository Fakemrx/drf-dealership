"""Models of provider app."""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Provider(models.Model):
    """
    Model of provider, includes name, foundation year, status (active or not).
    """

    name = models.CharField(max_length=100, verbose_name="Naming")
    foundation_year = models.IntegerField(verbose_name="Year of foundation")
    is_active = models.BooleanField(verbose_name="Is active")

    def __str__(self):
        result = f"{self.name} | {self.foundation_year} | "
        if self.is_active is False:
            result += "Inactive"
        else:
            result += "Active"
        return result


class CarsInProviderStock(models.Model):
    """
    Model of availability cars in providers stock, includes a provider, car, price of each vehicle.
    """

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Car price"
    )

    def __str__(self):
        return f"Provider {self.provider.name} has {self.car}. Price: {self.price}"


class ProviderDiscounts(models.Model):
    """
    Model of discounts, includes a provider, car, discount dates,
    discount in percentage, name of discount and description.
    """

    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Provider"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    discount_dates = models.DurationField(verbose_name="Dates of promotion")
    discount = models.DecimalField(
        max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR
    )
    name = models.CharField(max_length=100, verbose_name="Promotion naming")
    description = models.CharField(
        max_length=1000, verbose_name="Promotion description"
    )
