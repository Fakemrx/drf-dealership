"""Serializers module for Offer model."""
from rest_framework import serializers

from buyer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""

    class Meta:
        model = Offer
        fields = "__all__"
