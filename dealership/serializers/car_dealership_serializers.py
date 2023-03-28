"""Serializers module for CarDealership model."""
from rest_framework import serializers

from dealership.models import CarDealership


class CarDealershipSerializer(serializers.ModelSerializer):
    """Serializer for CarDealership model."""

    class Meta:
        model = CarDealership
        fields = "__all__"
