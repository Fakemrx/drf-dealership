"""
Car app testing module for correct data responses during filtration,
sorting and searching engines by its fields.
"""
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from car.models import Engine
from car.serializers.engine_serializers import EngineSerializer

c = APIClient()


@pytest.fixture
def engine():
    """Fixture to add 3 engine instances."""
    engine1 = Engine.objects.create(
        id=1,
        engine_brand="Brand1",
        fuel_type="gas",
        engine_volume=1.6,
        hp=160,
        is_active=True,
    )
    engine2 = Engine.objects.create(
        id=2,
        engine_brand="2Brand",
        fuel_type="gas",
        engine_volume=2.4,
        hp=120,
        is_active=False,
    )
    engine3 = Engine.objects.create(
        id=3,
        engine_brand="Brand3",
        fuel_type="electro",
        engine_volume=2.7,
        hp=105,
        is_active=False,
    )
    return [engine1, engine2, engine3]


@pytest.mark.django_db
def test_engine_search_filter(engine):
    """Testing if the search filter will provide correct data filtration for engines list page."""
    response = c.get("/api/cars/engines/?search=Brand")
    serializer_data = EngineSerializer((engine[0], engine[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_fuel_filter(engine):
    """
    Testing if the fuel_type field filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?fuel_type=gas")
    serializer_data = EngineSerializer((engine[1], engine[0]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_range_filter(engine):
    """
    Testing if the volume min and max filters will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?engine_volume_min=2.1&engine_volume_max=2.5")
    serializer_data = EngineSerializer(engine[1]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_min_filter(engine):
    """
    Testing if the volume min filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?engine_volume_min=2.4")
    serializer_data = EngineSerializer((engine[1], engine[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_max_filter(engine):
    """
    Testing if the volume max filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?engine_volume_max=1.6")
    serializer_data = EngineSerializer(engine[0]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_min_and_max_filter(engine):
    """
    Testing if the H.P. min and max filters will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?hp_min=100&hp_max=120")
    serializer_data = EngineSerializer((engine[1], engine[2]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_hp_min_filter(engine):
    """
    Testing if the H.P. min filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?hp_min=110")
    serializer_data = EngineSerializer((engine[1], engine[0]), many=True).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_hp_max_filter(engine):
    """
    Testing if the H.P. max filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?hp_max=115")
    serializer_data = EngineSerializer(engine[2]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_is_active_filter(engine):
    """
    Testing if the is_active field filter will provide
    correct data filtration for engines list page.
    """
    response = c.get("/api/cars/engines/?is_active=True")
    serializer_data = EngineSerializer(engine[0]).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data[0] == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_hp_ascending_ordering(engine):
    """
    Testing if the H.P. ascending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=hp")
    serializer_data = EngineSerializer(
        (engine[2], engine[1], engine[0]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_hp_descending_ordering(engine):
    """
    Testing if the H.P. descending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=-hp")
    serializer_data = EngineSerializer(
        (engine[0], engine[1], engine[2]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_ascending_ordering(engine):
    """
    Testing if the volume ascending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=engine_volume")
    serializer_data = EngineSerializer(
        (engine[0], engine[1], engine[2]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_volume_descending_ordering(engine):
    """
    Testing if the volume descending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=-engine_volume")
    serializer_data = EngineSerializer(
        (engine[2], engine[1], engine[0]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_brand_ascending_ordering(engine):
    """
    Testing if the brand ascending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=engine_brand")
    serializer_data = EngineSerializer(
        (engine[1], engine[0], engine[2]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"


@pytest.mark.django_db
def test_engine_brand_descending_ordering(engine):
    """
    Testing if the brand descending sort tool will provide
    correct data sorting for engines list page.
    """
    response = c.get("/api/cars/engines/?ordering=-engine_brand")
    serializer_data = EngineSerializer(
        (engine[2], engine[0], engine[1]), many=True
    ).data
    assert response.status_code == status.HTTP_200_OK, "Should be 200"
    assert response.data == serializer_data, "Should be equal"
