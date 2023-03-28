"""Serializers module for Provider model."""
from rest_framework import serializers

from provider.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer for Provider model."""

    class Meta:
        model = Provider
        fields = "__all__"
