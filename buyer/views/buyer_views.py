"""Module of CRUD APIViews for Buyer model."""
from django.contrib import auth
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from buyer.filters import BuyerFilter
from buyer.models import Buyer
from buyer.serializers.buyer_serializers import (
    BuyerSerializer,
    RegistrationSerializer,
    AuthSerializer,
)
from buyer.services import create_buyer_and_user

User = get_user_model()


class BuyerRetrieveAPIView(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """APIView for list and detail operations with Buyer model."""

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


class RegistrationAPIView(APIView):
    """APIView for create operation with User-Buyer model."""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Post method to create User-Buyer instances."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        create_buyer_and_user(validated_data)
        user = User.objects.get(id=validated_data["id"])
        token = Token.objects.get_or_create(user=user)[0]
        return Response(
            {"token": str(token), "user_id": user.id}, status=status.HTTP_201_CREATED
        )


class AuthAPIView(APIView):
    """APIView for authentication."""

    serializer_class = AuthSerializer

    def post(self, request):
        """Post method to create User-Buyer instances."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        user = auth.authenticate(
            request,
            username=validated_data["username"],
            password=validated_data["password"],
        )
        if user is None:
            raise serializers.ValidationError({"password": "Invalid password"})
        auth.login(request, user)
        return Response({"username": user.username}, status=status.HTTP_200_OK)
