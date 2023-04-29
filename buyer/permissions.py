"""Permission's for Buyer views"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission that checks is user that tries to change data
    is the same user as data/account owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.path.startswith("/api/buyer/buyers/balance/"):
            return request.user.id == obj.account.id
        if request.path.startswith("/api/buyer/offers/"):
            return request.user.id == obj.buyer.account.id
        if request.path.startswith(f"/api/buyer/buyers/{obj.id}/"):
            return request.user.id == obj.account.id
        return False
