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
    price during discount, name of discount and description.
    """

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Provider"
    )
    car = models.ForeignKey(
        CarsInProviderStock, on_delete=models.CASCADE, verbose_name="Car in stock"
    )
    discount_date_from = models.DateField(verbose_name="Date of promotion start")
    discount_date_to = models.DateField(verbose_name="Date of promotion ending")
    price_during_discount = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Car price during discount"
    )
    name = models.CharField(max_length=100, verbose_name="Promotion naming")
    description = models.CharField(
        max_length=1000, verbose_name="Promotion description"
    )

    def __str__(self):
        return (
            f"{self.provider.name} have a discount from {self.discount_date_from} to "
            f"{self.discount_date_to} a {self.car.car} - {self.price_during_discount} USD"
        )


class ProviderPersonalDiscounts(models.Model):
    """Model of personal discounts according to quantity of bought cars."""

    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Provider"
    )
    dealership = models.ForeignKey(
        "dealership.CarDealership", on_delete=models.CASCADE, verbose_name="Dealership"
    )
    actual_discount = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR, verbose_name="Actual discount"
    )
    quantity_of_bought_cars = models.IntegerField(
        verbose_name="Quantity of bought cars"
    )

    def __str__(self):
        return (
            f"For all time {self.dealership.name} bought {self.quantity_of_bought_cars}"
            f" cars from {self.provider.name}. Actual discount - {self.actual_discount}"
        )


class ProviderSales(models.Model):
    """
    Model of provider buyer's (dealerships only), includes a provider, dealership, car,
    quantity of vehicles, total price, date.
    """

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Provider"
    )
    dealership = models.ForeignKey(
        "dealership.CarDealership", on_delete=models.CASCADE, verbose_name="Dealership"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    quantity = models.IntegerField(verbose_name="Quantity of cars")
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Total price"
    )
    sell_date = models.DateTimeField(auto_now=True, verbose_name="Date of sale")

    def __str__(self):
        return (
            f"{self.provider.name} sold {self.quantity} {self.car} to "
            f"{self.dealership.name} with total price: {self.total_price} USD |"
            f"{self.sell_date}"
        )
