"""Serializers testing module to check correct adding data through them"""
import random

import pytest

from car.models import Engine, Car
from car.serializers.car_serializers import CarSerializer
from car.serializers.engine_serializers import EngineSerializer


@pytest.mark.django_db
def test_engine_serializer():
    """Test function to check if EngineSerializer works correctly."""
    engine_choices = (
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
    tank_choices = (
        ("gas", "Gasoline"),
        ("diesel", "Diesel"),
        ("hybrid", "Hybrid"),
        ("electro", "Electro"),
        ("etc", "Etc."),
    )
    fuel_type_data = random.choice(tank_choices)[0]
    engine_type_data = random.choice(engine_choices)[0]
    engine_volume_data = random.uniform(1.0, 7.0)
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type=fuel_type_data,
        engine_type=engine_type_data,
        engine_volume=engine_volume_data,
        hp=111,
        torque=112,
        is_active=True,
    )
    serializer_data = EngineSerializer(engine).data
    expected_data = {
        "id": engine.id,
        "engine_brand": "Test-Brand",
        "fuel_type": fuel_type_data,
        "engine_type": engine_type_data,
        "engine_volume": str(round(engine_volume_data, 1)),
        "hp": 111,
        "torque": 112,
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_car_serializer():
    """Test function to check if CarSerializer works correctly."""
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type="gas",
        engine_type="i3",
        engine_volume="3.1",
        hp=311,
        torque=312,
        is_active=True,
    )
    car = Car.objects.create(
        car_brand="Car test brand",
        car_model="Test model",
        release_year=2022,
        car_type="suv",
        engine=engine,
        gearbox_type="m",
        drivetrain_type="awd",
        seat_places=5,
        is_active=True,
    )
    serializer_data = CarSerializer(car).data
    expected_data = {
        "id": car.id,
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "gearbox_type": "m",
        "drivetrain_type": "awd",
        "seat_places": 5,
        "is_active": True,
    }
    assert serializer_data == expected_data
