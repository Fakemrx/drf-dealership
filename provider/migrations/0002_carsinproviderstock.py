# Generated by Django 4.1.7 on 2023-03-13 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("car", "0001_initial"),
        ("provider", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarsInProviderStock",
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
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="Car price"
                    ),
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
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.provider",
                        verbose_name="Dealership",
                    ),
                ),
            ],
        ),
    ]
