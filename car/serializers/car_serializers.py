"""Serializers module for Car model."""
from rest_framework import serializers

from car.models import Car


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model."""

    class Meta:
        model = Car
        fields = "__all__"
