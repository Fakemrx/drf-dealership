"""Models of dealership app."""
from django.core.validators import MinValueValidator, MaxValueValidator
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


class CarsInDealershipStock(models.Model):
    """
    Model of availability of cars in dealership's stock, includes dealership, car,
    quantity of vehicles in stock and price of each one.
    """

    dealership = models.ForeignKey(
        CarDealership, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    quantity = models.IntegerField(verbose_name="Quantity of cars")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Car price"
    )

    def __str__(self):
        return (
            f"{self.dealership.name} has {self.quantity} {self.car} | {self.price} USD"
        )


class DealershipDiscounts(models.Model):
    """
    Model of discounts, includes a dealer, car, discount dates,
    price during discount, name of discount and description.
    """

    dealer = models.ForeignKey(
        CarDealership, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    car = models.ForeignKey(
        CarsInDealershipStock, on_delete=models.CASCADE, verbose_name="Car in stock"
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
            f"{self.dealer.name} have a discount from {self.discount_date_from} to "
            f"{self.discount_date_to} a {self.car.car} - {self.price_during_discount} USD"
        )


class DealershipPersonalDiscounts(models.Model):
    """Model of personal discounts according to quantity of bought cars."""

    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    dealer = models.ForeignKey(
        CarDealership, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    buyer = models.ForeignKey(
        "buyer.Buyer", on_delete=models.CASCADE, verbose_name="Buyer"
    )
    actual_discount = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR, verbose_name="Actual discount"
    )
    quantity_of_bought_cars = models.IntegerField(
        verbose_name="Quantity of bought cars"
    )

    def __str__(self):
        return (
            f"For all time {self.buyer.account.name} bought {self.quantity_of_bought_cars}"
            f" cars from {self.dealer.name}. Actual discount - {self.actual_discount}"
        )


class DealerSales(models.Model):
    """
    Model of dealer buyer's (buyers only), includes a dealer, buyer, car,
    quantity of vehicles, total price, date.
    """

    dealer = models.ForeignKey(
        CarDealership, on_delete=models.CASCADE, verbose_name="Dealership"
    )
    buyer = models.ForeignKey(
        "buyer.Buyer", on_delete=models.CASCADE, verbose_name="Buyer"
    )
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, verbose_name="Car")
    quantity = models.IntegerField(verbose_name="Quantity of cars")
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Total price"
    )
    sell_date = models.DateTimeField(auto_now=True, verbose_name="Date of sale")

    def __str__(self):
        return (
            f"{self.dealer.name} sold {self.quantity} {self.car} to "
            f"{self.buyer.account.name} with total price: {self.total_price} USD |"
            f"{self.sell_date}"
        )
