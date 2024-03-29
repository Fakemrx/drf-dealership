"""Module of CRUD APIViews for Offer model."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from buyer.filters import OfferFilter
from buyer.models import Offer, Buyer
from buyer.permissions import IsOwner
from buyer.serializers.offer_serializers import OfferSerializer


class OfferAPIView(ModelViewSet):
    """APIView for CRUD operations with Offer model."""

    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Offer.objects.select_related("buyer", "car").filter(is_active=True)
    serializer_class = OfferSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^buyer__full_name", "^car__brand"]
    ordering_fields = ["max_cost"]
    ordering = ["max_cost"]
    filterset_class = OfferFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={
                "buyer": Buyer.objects.filter(account=request.user)
                .select_related("account")
                .first()
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data})
