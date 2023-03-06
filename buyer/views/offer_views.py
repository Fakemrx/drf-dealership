"""Module of CRUD APIViews for Offer model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from buyer.filters import OfferFilter
from buyer.models import Offer
from buyer.serializers.offer_serializers import OfferSerializer


class OfferAPIView(ModelViewSet):
    """APIView for CRUD operations with Offer model."""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^buyer__full_name", "^car__brand"]
    ordering_fields = ["max_cost", "quantity"]
    ordering = ["max_cost"]
    filterset_class = OfferFilter
