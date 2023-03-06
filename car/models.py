"""Models of car app."""
from django.db import models


class Car(models.Model):
    """
    Model of car, includes car brand, model, release year, types such as: car, gearbox,
    drivetrain, engine, also seat places and car status (active or not).
    """

    class CarTypes(models.TextChoices):
        """Car types choices."""

        suv = ("suv", "SUV")
        sedan = ("sedan", "Sedan 4-d")
        coupe = ("coupe", "Coupe 2-d")
        sport = ("sport", "Sportcar")
        hyper = ("hyper", "Hypercar")
        minivan = ("minivan", "Mini-van")
        van = ("van", "Van")
        truck = ("truck", "Truck")
        wagon = ("wagon", "Wagon")
        muscle = ("muscle", "Musclecar")
        etc = ("etc", "Etc.")

    car_brand = models.CharField(max_length=30, verbose_name="Car brand")
    car_model = models.CharField(max_length=50, verbose_name="Car model")
    release_year = models.IntegerField(verbose_name="Release year")
    car_type = models.CharField(
        choices=CarTypes.choices, max_length=7, verbose_name="Car type"
    )
    engine = models.ForeignKey("car.Engine", null=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return f"{self.car_brand} {self.car_model} {self.release_year}"


class Engine(models.Model):
    """
    Model of engine, attached to some cars, includes fuel type,
    engine type, volume, H.P., torque.
    """

    class TankTypes(models.TextChoices):
        """Tank types choices."""

        gas = ("gas", "Gasoline")
        diesel = ("diesel", "Diesel")
        hybrid = ("hybrid", "Hybrid")
        electro = ("electro", "Electro")
        etc = ("etc", "Etc.")

    engine_brand = models.CharField(max_length=30, verbose_name="Engine brand")
    fuel_type = models.CharField(
        choices=TankTypes.choices, max_length=7, verbose_name="Fuel type"
    )
    engine_volume = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Engine volume"
    )
    hp = models.IntegerField(null=True, blank=True, verbose_name="Engine horse powers")
    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return (
            f"{self.engine_brand} {self.engine_volume} l. | "
            f"{self.fuel_type} | {self.hp} h.p."
        )
