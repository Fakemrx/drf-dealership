# Generated by Django 4.1.7 on 2023-02-21 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("car", "0002_alter_car_car_type_alter_car_drivetrain_type_and_more"),
    ]

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
                        max_length=7,
                        verbose_name="Fuel type",
                    ),
                ),
                (
                    "engine_type",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=3,
                        verbose_name="Engine type",
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
                    "torque",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Engine torque"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="car",
            name="engine_type",
        ),
        migrations.RemoveField(
            model_name="car",
            name="engine_volume",
        ),
        migrations.RemoveField(
            model_name="car",
            name="fuel_type",
        ),
        migrations.RemoveField(
            model_name="car",
            name="hp",
        ),
        migrations.RemoveField(
            model_name="car",
            name="torque",
        ),
        migrations.AlterField(
            model_name="car",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AddField(
            model_name="car",
            name="engine",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="car.engine"
            ),
        ),
    ]
