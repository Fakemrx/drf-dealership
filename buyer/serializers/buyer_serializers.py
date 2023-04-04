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

    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Buyer
        fields = "__all__"


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

    @staticmethod
    def validate_password(password):
        """Validation for password field."""
        if len(password) < 8:
            raise serializers.ValidationError("Minimal password length - 8 symbols")
        if not re.search("[a-z]", password):
            raise serializers.ValidationError(
                f"Password must contain at least 1 {ascii_lowercase} letter"
            )
        if not re.search("[A-Z]", password):
            raise serializers.ValidationError(
                f"Password must contain at least 1 {ascii_uppercase} letter"
            )
        if not re.search("[0-9]", password):
            raise serializers.ValidationError("Password must contain at least 1 digit")
        return password

    @staticmethod
    def validate_email(email):
        """Validation for email field."""
        try:
            email_validator(email)
        except ValidationError:
            raise serializers.ValidationError(
                "The email is not a valid email address."
            ) from ValidationError
        return email

    @staticmethod
    def validate_username(username):
        """Validation for username field."""
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f"User {username} already exists.")
        return username

    @staticmethod
    def validate_first_name(first_name):
        """Validation for full_name field."""
        return first_name.capitalize()

    @staticmethod
    def validate_last_name(last_name):
        """Validation for full_name field."""
        return last_name.capitalize()
