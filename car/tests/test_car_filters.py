"""
Car app testing module for correct data responses during filtration,
sorting and searching cars by its fields.
"""
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from car.models import Engine, Car
from car.serializers.car_serializers import CarSerializer

c = APIClient()


@pytest.fixture
def car():
    """Fixture to add 3 car instances."""
    engine = Engine.objects.create(
        id=1,
        engine_brand="Brand1",
        fuel_type="gas",
        engine_volume=1.6,
        hp=160,
        is_active=True,
    )
    car1 = Car.objects.create(
        id=1,
        car_brand="BMW",
        car_model="E 330i",
        release_year=2020,
        car_type="sedan",
        engine=engine,
        is_active=True,
    )
    car2 = Car.objects.create(
        id=2,
        car_brand="Mercedes",
        car_model="E63",
        release_year=2018,
        car_type="coupe",
        engine=engine,
        is_active=False,
    )
    car3 = Car.objects.create(
        id=3,
        car_brand="BMW",
        car_model="M4",
        release_year=2019,
        car_type="sport",
        engine=engine,
        is_active=True,
    )
    return [car1, car2, car3]


@pytest.mark.django_db
def test_car_search_filter(car):
    """Testing if the search filter will provide correct data filtration for cars list page."""
    response = c.get("/api/cars/?search=BMW")
    serializer_data = CarSerializer((car[0], car[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"

    response = c.get("/api/cars/?search=E")
    serializer_data = CarSerializer((car[0], car[1]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_type_filter(car):
    """
    Testing if the car_type field filter will provide
    correct data filtration for cars list page.
    """
    response = c.get("/api/cars/?car_type=coupe")
    serializer_data = CarSerializer(car[1]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"

    response = c.get("/api/cars/?car_type=sport")
    serializer_data = CarSerializer(car[2]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_year_min_and_max_filter(car):
    """
    Testing if the release_year min and max filters will provide
    correct data filtration for cars list page.
    """
    response = c.get("/api/cars/?release_year_min=2018&release_year_max=2019")
    serializer_data = CarSerializer((car[2], car[1]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_year_min_filter(car):
    """
    Testing if the release_year min filter will provide
    correct data filtration for cars list page.
    """
    response = c.get("/api/cars/?release_year_min=2019")
    serializer_data = CarSerializer((car[0], car[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_year_max_filter(car):
    """
    Testing if the release_year max filter will provide
    correct data filtration for cars list page.
    """
    response = c.get("/api/cars/?release_year_max=2018")
    serializer_data = CarSerializer(car[1]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_is_active_filter(car):
    """
    Testing if the is_active field filter will provide
    correct data filtration for cars list page.
    """
    response = c.get("/api/cars/?is_active=True")
    serializer_data = CarSerializer((car[0], car[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_year_ascending_ordering(car):
    """
    Testing if the year ascending sort tool will provide
    correct data sorting for cars list page.
    """
    response = c.get("/api/cars/?ordering=release_year")
    serializer_data = CarSerializer((car[1], car[2], car[0]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_year_descending_ordering(car):
    """
    Testing if the H.P. descending sort tool will provide
    correct data sorting for cars list page.
    """
    response = c.get("/api/cars/?ordering=-release_year")
    serializer_data = CarSerializer((car[0], car[2], car[1]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_brand_ascending_ordering(car):
    """
    Testing if the brand ascending sort tool will provide
    correct data sorting for cars list page.
    """
    response = c.get("/api/cars/?ordering=car_brand")
    serializer_data = CarSerializer((car[0], car[2], car[1]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_car_brand_descending_ordering(car):
    """
    Testing if the brand descending sort tool will provide
    correct data sorting for cars list page.
    """
    response = c.get("/api/cars/?ordering=-car_brand")
    serializer_data = CarSerializer((car[1], car[0], car[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"
