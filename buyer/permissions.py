"""Permission's for Buyer views"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission that checks is user, that wants to increase balance
    the same as user, that owns an account.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.account.id
