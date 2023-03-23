"""Buyer's app services."""
from django.contrib.auth import get_user_model

from buyer.models import Buyer

User = get_user_model()


def create_buyer_and_user(request):
    """Create user and after that create buyer with reference to user."""
    validated_data = request.data
    user = User(
        username=validated_data["username"],
        email=validated_data["email"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
    )
    user.set_password(validated_data["password"])
    user.save()
    Buyer.objects.create(
        account=user,
        age=validated_data["age"],
        gender=validated_data["gender"],
        balance=0.00,
        is_active=True,
    )
