"""Serializers module for Offer model."""
from rest_framework import serializers

from buyer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""

    id = serializers.IntegerField(read_only=True)
    buyer = serializers.CharField(read_only=True)
    max_cost = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=8)
    is_active = serializers.HiddenField(default=True)

    def validate(self, attrs):
        """
        Check that the max_cost is lower than buyer's balance.
        """
        attrs["buyer"] = self.context["buyer"]
        if attrs["max_cost"] > attrs["buyer"].balance:
            raise serializers.ValidationError(
                {
                    "max_cost": f"You don't have enough "
                    f"money, value should be under "
                    f"{attrs['buyer'].balance}"
                }
            )
        return attrs

    class Meta:
        model = Offer
        fields = "__all__"
