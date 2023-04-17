"""Serializers module for Offer model."""
from rest_framework import serializers

from buyer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""

    id = serializers.IntegerField(read_only=True)
    buyer = serializers.CharField(read_only=True)
    max_cost = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=8)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Offer
        fields = "__all__"
