"""Car app testing module for correct responses, correct crud operations with data."""
import random
import pytest

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from car.models import Engine, Car
from car.serializers.car_serializers import CarSerializer
from car.serializers.engine_serializers import EngineSerializer

factory = APIRequestFactory()
c = APIClient()


@pytest.mark.django_db
def test_non_existing_car_detail():
    """
    Testing if the car retrieve/update/destroy page with an ID 1 will raise 404 error.
    """
    response = c.get("/api/cars/1/")
    assert response.status_code == 404, "Should be 404"


@pytest.mark.django_db
def test_non_existing_engine_detail():
    """
    Testing if the engine retrieve/update/destroy page with an ID 1 will raise 404 error.
    """
    response = c.get("/api/cars/engines/1/")
    assert response.status_code == 404, "Should be 404"


@pytest.mark.django_db
def test_new_engine_adding():
    """Testing if the new engine will be added with valid values."""
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
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type=random.choice(tank_choices)[0],
        engine_type=random.choice(engine_choices)[0],
        engine_volume=random.uniform(1.0, 7.0),
        hp=random.randint(70, 600),
        torque=random.randint(70, 600),
        is_active=bool(random.getrandbits(1)),
    )
    response = c.get("/api/cars/engines/")
    serializer_data = EngineSerializer(engine).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_new_car_adding():
    """Testing if the new car will be added with valid values."""
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
    response = c.get("/api/cars/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"
