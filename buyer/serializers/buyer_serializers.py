"""Serializers module for Buyer model."""
import re

from string import ascii_uppercase, ascii_lowercase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as email_validator
from rest_framework import serializers

from buyer.models import Buyer, Genders

User = get_user_model()


class BuyerSerializer(serializers.ModelSerializer):
    """Serializer for Buyer model."""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = User.objects.get(id=data["account"])
        data["username"] = user.username
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["email"] = user.email
        return data

    class Meta:
        model = Buyer
        fields = ["account", "age", "gender", "balance", "is_active"]


class RegistrationSerializer(serializers.Serializer):
    """Serializer for User model."""

    id = serializers.ReadOnlyField()
    username = serializers.CharField(min_length=3, max_length=20)
    password = serializers.CharField(style={"input_type": "password"})
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField(min_value=16, max_value=100)
    gender = serializers.ChoiceField(
        choices=[(gender.name, gender.value) for gender in Genders]
    )

    def validate_password(self, value):
        """Validation for password field."""
        if len(value) < 8:
            raise serializers.ValidationError("Minimal password length - 8 symbols")
        if not re.search("[a-z]", value):
            raise serializers.ValidationError(
                f"Password must contain at least 1 {ascii_lowercase} letter"
            )
        if not re.search("[A-Z]", value):
            raise serializers.ValidationError(
                f"Password must contain at least 1 {ascii_uppercase} letter"
            )
        if not re.search("[0-9]", value):
            raise serializers.ValidationError("Password must contain at least 1 digit")
        return value

    def validate_email(self, value):
        """Validation for email field."""
        try:
            email_validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "The email is not a valid email address."
            ) from ValidationError
        return value

    def validate_username(self, value):
        """Validation for username field."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"User {value} already exists.")
        return value

    def validate_first_name(self, value):
        """Validation for full_name field."""
        return value.capitalize()

    def validate_last_name(self, value):
        """Validation for full_name field."""
        return value.capitalize()
