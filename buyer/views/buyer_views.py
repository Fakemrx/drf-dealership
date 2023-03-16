"""Module of CRUD APIViews for Buyer model."""
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from buyer.filters import BuyerFilter
from buyer.models import Buyer
from buyer.serializers.buyer_serializers import BuyerSerializer, UserSerializer

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


class UserAPIView(APIView):
    """APIView for create operation with User-Buyer model."""

    serializer_class = UserSerializer

    def post(self, request):
        """Post method to create User-Buyer instances."""
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        validated_data = request.data
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Buyer.objects.create(
            account=user,
            full_name=validated_data["full_name"],
            age=validated_data["age"],
            gender=validated_data["gender"],
            balance=0.00,
            is_active=True,
        )
        return Response(data=request.data, status=status.HTTP_201_CREATED)
