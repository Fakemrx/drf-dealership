"""Serializers module for Buyer model."""
from rest_framework import serializers

from buyer.models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    """Serializer for Buyer model."""

    class Meta:
        model = Buyer
        fields = "__all__"