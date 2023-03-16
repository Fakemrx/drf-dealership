"""Serializers module for Buyer model."""
import re
from string import ascii_uppercase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as email_validator
from rest_framework import serializers

from buyer.models import Buyer, Genders

User = get_user_model()


class BuyerSerializer(serializers.ModelSerializer):
    """Serializer for Buyer model."""

    class Meta:
        model = Buyer
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(
        choices=[(gender.name, gender.value) for gender in Genders]
    )

    def validate_password(self, value):
        """Validation for password field."""
        if len(value) < 8:
            raise serializers.ValidationError("Minimal password length - 8 symbols")
        if not re.search("[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 [a-z] letter"
            )
        if not re.search("[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 [A-Z] letter"
            )
        if not re.search("[0-9]", value):
            raise serializers.ValidationError("Password must contain at least 1 digit")
        print(value)
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
        if len(value) <= 3:
            raise serializers.ValidationError(
                "Too short, there should be more than 3 characters."
            )
        if len(value) > 20:
            raise serializers.ValidationError(
                "Too long, there should not be more than 20 characters."
            )
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError(f"User {value} already exists.")
        except User.DoesNotExist:
            return value

    def validate_age(self, value):
        """Validation for age field."""
        if value <= 0:
            raise serializers.ValidationError("Age must be positive.")
        if value <= 16:
            raise serializers.ValidationError("Too young to become a buyer.")
        if value >= 100:
            raise serializers.ValidationError("False information.")

    def validate_full_name(self, value):
        """Validation for full_name field."""
        if len(value.split(" ")) != 3:
            raise serializers.ValidationError("Incorrect full name format.")
        for word in value.split(" "):
            if word[0] not in ascii_uppercase:
                raise serializers.ValidationError(
                    "The first letters must be in an upper case."
                )

    class Meta:
        model = Buyer
        fields = ["username", "password", "email", "full_name", "age", "gender"]
