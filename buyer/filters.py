"""Custom filters for buyer app."""
from django_filters import rest_framework as filters

from buyer.models import Buyer, Offer, Genders


class BuyerFilter(filters.FilterSet):
    """Custom filtering for Buyer model list."""

    gender = filters.ChoiceFilter(
        choices=[(gender.name, gender.value) for gender in Genders]
    )
    age = filters.RangeFilter()
    balance = filters.RangeFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = Buyer
        fields = ["gender", "age", "balance", "is_active"]


class OfferFilter(filters.FilterSet):
    """Custom filtering for Offer model list."""

    max_cost = filters.RangeFilter()
    quantity = filters.RangeFilter()

    class Meta:
        model = Offer
        fields = ["max_cost", "quantity"]
