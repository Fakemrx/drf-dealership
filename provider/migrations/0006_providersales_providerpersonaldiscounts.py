# Generated by Django 4.1.7 on 2023-03-21 06:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dealership", "0003_carsindealershipstock"),
        ("car", "0001_initial"),
        ("provider", "0005_remove_providerdiscounts_discount_dates_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProviderSales",
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
                ("quantity", models.IntegerField(verbose_name="Quantity of cars")),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="Total price"
                    ),
                ),
                (
                    "sell_date",
                    models.DateTimeField(auto_now=True, verbose_name="Date of sale"),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="car.car",
                        verbose_name="Car",
                    ),
                ),
                (
                    "dealership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.cardealership",
                        verbose_name="Dealership",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.provider",
                        verbose_name="Provider",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProviderPersonalDiscounts",
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
                    "actual_discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Actual discount",
                    ),
                ),
                (
                    "quantity_of_bought_cars",
                    models.IntegerField(verbose_name="Quantity of bought cars"),
                ),
                (
                    "dealership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.cardealership",
                        verbose_name="Dealership",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.provider",
                        verbose_name="Provider",
                    ),
                ),
            ],
        ),
    ]
