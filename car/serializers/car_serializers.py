"""Serializers module for Car model."""
from rest_framework import serializers

from car.models import Car


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model."""

    class Meta:
        model = Car
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["engine"] = str(instance.engine)
        return rep
