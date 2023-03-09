# Generated by Django 4.1.7 on 2023-03-09 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Engine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "engine_brand",
                    models.CharField(max_length=30, verbose_name="Engine brand"),
                ),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[
                            ("gas", "Gasoline"),
                            ("diesel", "Diesel"),
                            ("hybrid", "Hybrid"),
                            ("electro", "Electro"),
                            ("etc", "Etc."),
                        ],
                        max_length=20,
                        verbose_name="Fuel type",
                    ),
                ),
                (
                    "engine_volume",
                    models.DecimalField(
                        decimal_places=1, max_digits=3, verbose_name="Engine volume"
                    ),
                ),
                (
                    "hp",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Engine horse powers"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "car_brand",
                    models.CharField(max_length=30, verbose_name="Car brand"),
                ),
                (
                    "car_model",
                    models.CharField(max_length=50, verbose_name="Car model"),
                ),
                ("release_year", models.IntegerField(verbose_name="Release year")),
                (
                    "car_type",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=20,
                        verbose_name="Car type",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
                (
                    "engine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="car.engine",
                    ),
                ),
            ],
        ),
    ]
