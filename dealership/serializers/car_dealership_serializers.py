"""Serializers module for Dealership models."""
from rest_framework import serializers

from dealership.models import CarDealership, CarsInDealershipStock


class CarDealershipSerializer(serializers.ModelSerializer):
    """Serializer for CarDealership model."""

    class Meta:
        model = CarDealership
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["preferred_cars_list"] = [
            str(car) for car in instance.preferred_cars_list.all()
        ]
        return rep


class CarsInStockSerializer(serializers.ModelSerializer):
    """Serializer for CarsInDealershipStock model."""

    car = serializers.CharField()
    dealership = serializers.CharField()

    class Meta:
        model = CarsInDealershipStock
        fields = "__all__"
