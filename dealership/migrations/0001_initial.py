# Generated by Django 4.1.7 on 2023-03-13 11:49

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("car", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarDealership",
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
                ("name", models.CharField(max_length=100, verbose_name="Naming")),
                (
                    "location",
                    django_countries.fields.CountryField(
                        max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Car dealership's balance",
                    ),
                ),
                ("is_active", models.BooleanField(verbose_name="Is active")),
                (
                    "preferred_cars_list",
                    models.ManyToManyField(
                        to="car.car", verbose_name="List of preferred cars"
                    ),
                ),
            ],
        ),
    ]
