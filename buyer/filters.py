"""Custom filters for buyer app."""
from django_filters import rest_framework as filters

from buyer.models import Buyer


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
