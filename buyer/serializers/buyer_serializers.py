"""Serializers module for Buyer model."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from buyer.models import Buyer, Genders

User = get_user_model()


class BuyerSerializer(serializers.ModelSerializer):
    """Serializer for Buyer model."""

    class Meta:
        model = Buyer
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    """Serializer for User model."""

    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(
        choices=[(gender.name, gender.value) for gender in Genders]
    )
    balance = serializers.HiddenField(default=0.00)
    is_active = serializers.HiddenField(default=True)

    def create(self, validated_data):
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
            balance=validated_data["balance"],
            is_active=validated_data["is_active"],
        )
        return validated_data
