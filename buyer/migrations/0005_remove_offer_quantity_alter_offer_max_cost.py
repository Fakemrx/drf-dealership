# Generated by Django 4.2 on 2023-04-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("buyer", "0004_remove_buyer_full_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offer",
            name="quantity",
        ),
        migrations.AlterField(
            model_name="offer",
            name="max_cost",
            field=models.DecimalField(
                decimal_places=2, max_digits=8, verbose_name="Maximum cost"
            ),
        ),
    ]
