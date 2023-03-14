"""Serializers testing module to check correct adding data through them"""
import pytest

from car.serializers.car_serializers import CarSerializer
from car.serializers.engine_serializers import EngineSerializer
from tests.project_fixtures import engine, car


@pytest.mark.django_db
def test_engine_serializer(engine):
    """Test function to check if EngineSerializer works correctly."""
    serializer_data = EngineSerializer(engine).data
    expected_data = {
        "id": engine.id,
        "engine_brand": "Test-Brand",
        "fuel_type": "gas",
        "engine_volume": "1.5",
        "hp": 111,
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"


@pytest.mark.django_db
def test_car_serializer(car, engine):
    """Test function to check if CarSerializer works correctly."""
    serializer_data = CarSerializer(car).data
    expected_data = {
        "id": car.id,
        "car_brand": "Car test brand",
        "car_model": "Test model",
        "release_year": 2022,
        "car_type": "suv",
        "engine": engine.id,
        "is_active": True,
    }
    assert serializer_data == expected_data, "Should be equal"
