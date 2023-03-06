"""Custom filters for buyer app."""
from django_filters import rest_framework as filters

from buyer.models import Buyer, Offer


class BuyerFilter(filters.FilterSet):
    """Custom filtering for Buyer model list."""

    gender_choices = (("male", "Male"), ("female", "Female"))
    gender = filters.ChoiceFilter(choices=gender_choices)
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
