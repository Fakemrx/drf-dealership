"""Simplifies testing when user token is needed"""
from rest_framework.test import APIClient


def get_user_token(buyer):
    """Returns user access_token, useful for tests"""
    c = APIClient()
    user_token = c.post(
        "/api/buyer/token/",
        data={"username": buyer.account.username, "password": "TestPass123"},
    ).data["access"]
    return user_token
