"""Models of car app."""
from enum import Enum

from django.db import models


class CarTypes(Enum):
    """Car types choices."""

    suv = "SUV"
    sedan = "Sedan 4-d"
    coupe = "Coupe 2-d"
    sport = "Sportcar"
    hyper = "Hypercar"
    minivan = "Mini-van"
    van = "Van"
    truck = "Truck"
    wagon = "Wagon"
    muscle = "Musclecar"
    etc = "Etc."


class Car(models.Model):
    """
    Model of car, includes car brand, model, release year,
    car type, engine, car status (active or not).
    """

    car_brand = models.CharField(max_length=30, verbose_name="Car brand")
    car_model = models.CharField(max_length=50, verbose_name="Car model")
    release_year = models.IntegerField(verbose_name="Release year")
    car_type = models.CharField(
        choices=[(car_type.name, car_type.value) for car_type in CarTypes],
        max_length=20,
        verbose_name="Car type",
    )
    engine = models.ForeignKey("car.Engine", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return (
            f"Car {self.car_brand} {self.car_model} {self.release_year} | Type: "
            f"{CarTypes[f'{self.car_type}'].value} | Engine: {self.engine}"
        )


class TankTypes(Enum):
    """Tank types choices."""

    gas = "Gasoline"
    diesel = "Diesel"
    hybrid = "Hybrid"
    electro = "Electro"
    etc = "Etc."


class Engine(models.Model):
    """
    Model of engine, includes fuel type,
    engine type, volume, H.P..
    """

    engine_brand = models.CharField(max_length=30, verbose_name="Engine brand")
    fuel_type = models.CharField(
        choices=[(tank.name, tank.value) for tank in TankTypes],
        max_length=20,
        verbose_name="Fuel type",
    )
    engine_volume = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Engine volume"
    )
    hp = models.IntegerField(null=True, blank=True, verbose_name="Engine horse powers")

    def __str__(self):
        return (
            f"{self.engine_brand} {self.engine_volume} l. | "
            f"{self.fuel_type} | {self.hp} h.p."
        )
