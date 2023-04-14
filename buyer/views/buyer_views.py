"""Module of CRUD APIViews for Buyer model."""
from django.contrib.auth import get_user_model
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from buyer.filters import BuyerFilter
from buyer.models import Buyer
from buyer.permissions import IsSameUserAuthenticated
from buyer.serializers.buyer_serializers import (
    BuyerSerializer,
    RegistrationSerializer,
    BalanceSerializer,
)
from buyer.services import create_buyer_and_user

User = get_user_model()


class BuyerRetrieveAPIView(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """APIView for list and detail operations with Buyer model."""

    permission_classes = [IsSameUserAuthenticated]
    queryset = Buyer.objects.annotate(
        username=F("account__username"),
        email=F("account__email"),
        first_name=F("account__first_name"),
        last_name=F("account__last_name"),
    )
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


class RegistrationAPIView(APIView):
    """APIView for create operation with User-Buyer model."""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Post method to create User-Buyer instances."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        refresh_token, user_id = create_buyer_and_user(validated_data)
        return Response(
            {
                "refresh_token": str(refresh_token),
                "access_token": str(refresh_token.access_token),
                "user_id": user_id,
            },
            status=status.HTTP_201_CREATED,
        )


class BalanceUpdateAPIView(APIView):
    """APIView for changing balance. It gets access_token from headers,
    then it tries to check and find user, if it exists and no errors were
    occurred it will update buyer's balance."""

    permission_classes = [IsSameUserAuthenticated]
    serializer_class = BalanceSerializer

    def post(self, request):
        """Updates buyer's balance."""
        serializer = BalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = serializer.validated_data["value_of_money"]
        buyer = get_object_or_404(Buyer, account=request.user.id)

        buyer.balance += value
        buyer.save()

        return Response(
            {"message": f"{request.user}'s balance updated to {buyer.balance}"}
        )
