"""Module of CRUD APIViews for Buyer model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from buyer.filters import BuyerFilter
from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer


class BuyerAPIView(ModelViewSet):
    """APIView for CRUD operations with Buyer model."""

    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^full_name"]
    ordering_fields = ["age", "balance"]
    ordering = ["balance"]
    filterset_class = BuyerFilter
