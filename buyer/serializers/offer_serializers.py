"""Serializers module for Offer model."""
from rest_framework import serializers

from buyer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""

    id = serializers.IntegerField(read_only=True)
    buyer = serializers.CharField(read_only=True)
    max_cost = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=8)
    is_active = serializers.HiddenField(default=True)

    def create(self, validated_data):
        """Create method with validation for max_cost field"""
        if "buyer" in self.context.keys():
            validated_data["buyer"] = self.context["buyer"]
            if validated_data["max_cost"] > validated_data["buyer"].balance:
                raise serializers.ValidationError(
                    {
                        "max_cost": f"You don't have enough "
                        f"money, value should be under "
                        f"{validated_data['buyer'].balance}"
                    }
                )
        return Offer.objects.create(**validated_data)

    class Meta:
        model = Offer
        fields = "__all__"
