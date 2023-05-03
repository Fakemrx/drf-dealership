"""Serializers module for Engine model."""
from rest_framework import serializers

from car.models import Engine


class EngineSerializer(serializers.ModelSerializer):
    """Serializer for Engine model."""

    class Meta:
        model = Engine
        fields = "__all__"
