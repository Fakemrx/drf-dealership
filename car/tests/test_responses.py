"""Car app testing module for correct responses, correct crud operations with data."""
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from car.models import Engine, Car
from car.serializers.car_serializers import CarSerializer
from car.serializers.engine_serializers import EngineSerializer

c = APIClient()


@pytest.fixture
def engine():
    """Fixture to add engine instance."""
    engine = Engine.objects.create(
        engine_brand="Test-Brand",
        fuel_type="gas",
        engine_volume=1.5,
        hp=111,
        is_active=True,
    )
    return engine


@pytest.fixture
def car(engine):
    """Fixture to add car instance."""
    car = Car.objects.create(
        car_brand="Car test brand",
        car_model="Test model",
        release_year=2022,
        car_type="suv",
        engine=engine,
        is_active=True,
    )
    return car


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
def test_engine_add_detail(engine):
    """
    Testing if the new engine will be added
    with valid values and detail page will be available.
    """

    serializer_data = EngineSerializer(engine).data

    response = c.get("/api/cars/engines/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"

    response = c.get("/api/cars/engines/1/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_str(engine):
    """Testing if the __str__ for Engine model will return valid data."""
    assert str(engine) == "Test-Brand 1.5 l. | gas | 111 h.p.", "Should be equal"


@pytest.mark.django_db
def test_car_str(car):
    """Testing if the __str__ for Engine model will return valid data."""
    assert str(car) == "Car test brand Test model 2022", "Should be equal"


@pytest.mark.django_db
def test_car_add_detail(car):
    """Testing if the new car will be added with valid values and detail page will be available."""

    serializer_data = CarSerializer(car).data

    response = c.get("/api/cars/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"

    response = c.get("/api/cars/1/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"
