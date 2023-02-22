"""Models of car app."""
from django.db import models


class Car(models.Model):
    """
    Model of car, includes car brand, model, release year, types such as: car, fuel, gearbox,
    drivetrain, engine, also engine volume, H.P., torque, seat places and car status
    (active or not).
    """

    TYPE_CHOICES = (
        ("suv", "SUV"),
        ("sedan", "Sedan 4-d"),
        ("coupe", "Coupe 2-d"),
        ("sport", "Sportcar"),
        ("hyper", "Hypercar"),
        ("minivan", "Mini-van"),
        ("van", "Van"),
        ("truck", "Truck"),
        ("wagon", "Wagon"),
        ("muscle", "Musclecar"),
        ("etc", "Etc."),
    )
    GEARBOX_CHOICES = (
        ("m", "Manual"),
        ("a", "Automatic"),
        ("r", "Robotic"),
        ("v", "Variable"),
        ("s", "Sequental"),
        ("e", "Etc."),
    )
    DRIVETRAIN_CHOICES = (
        ("awd", "AWD"),
        ("fwd", "FWD"),
        ("rwd", "RWD"),
        ("4wd", "4WD"),
        ("etc", "Etc."),
    )

    car_brand = models.CharField(max_length=30, verbose_name="Car brand")
    car_model = models.CharField(max_length=50, verbose_name="Car model")
    release_year = models.IntegerField(verbose_name="Release year")
    car_type = models.CharField(
        choices=TYPE_CHOICES, max_length=7, verbose_name="Car type"
    )
    engine = models.ForeignKey("car.Engine", null=True, on_delete=models.SET_NULL)
    gearbox_type = models.CharField(
        choices=GEARBOX_CHOICES, max_length=1, verbose_name="Gearbox type"
    )
    drivetrain_type = models.CharField(
        choices=DRIVETRAIN_CHOICES, max_length=3, verbose_name="Drivetrain type"
    )
    seat_places = models.IntegerField(null=True, blank=True, verbose_name="Seat places")

    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return f"{self.car_brand} {self.car_model} {self.release_year}"


class Engine(models.Model):
    """
    Model of engine, attached to some cars, includes fuel type,
    engine type, volume, H.P., torque.
    """

    ENGINE_CHOICES = (
        ("i3", "I3"),
        ("i4", "I4"),
        ("i5", "I5"),
        ("i6", "I6"),
        ("v6", "V6"),
        ("v8", "V8"),
        ("v10", "V10"),
        ("v12", "V12"),
        ("w10", "W10"),
        ("w12", "W12"),
        ("e", "E"),
        ("etc", "Etc."),
    )
    TANK_CHOICES = (
        ("gas", "Gasoline"),
        ("diesel", "Diesel"),
        ("hybrid", "Hybrid"),
        ("electro", "Electro"),
        ("etc", "Etc."),
    )

    engine_brand = models.CharField(max_length=30, verbose_name="Engine brand")
    fuel_type = models.CharField(
        choices=TANK_CHOICES, max_length=7, verbose_name="Fuel type"
    )
    engine_type = models.CharField(
        choices=ENGINE_CHOICES, max_length=3, verbose_name="Engine type"
    )
    engine_volume = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Engine volume"
    )
    hp = models.IntegerField(null=True, blank=True, verbose_name="Engine horse powers")
    torque = models.IntegerField(null=True, blank=True, verbose_name="Engine torque")
    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return (
            f"{self.engine_brand} {self.engine_type} {self.engine_volume} l. | "
            f"{self.fuel_type} | {self.hp} h.p. | "
            f"{self.torque} nm."
        )
