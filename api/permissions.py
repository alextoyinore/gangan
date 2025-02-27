from datetime import timedelta, timezone
from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow creating new users if not authenticated.
    For all other operations, user must be authenticated.
    """

    def has_permission(self, request, view):
        # Allow all users to create new accounts
        if view.action == 'create':
            return True
        # For all other actions, only allow authenticated users
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the account
        if view.action == 'destroy':
            return obj == request.user
        # For all other actions, only allow authenticated users
        return (request.user and request.user.is_authenticated) or request.user.is_superuser


class IsAuthenticatedAndOwnerOnDelete(permissions.BasePermission):
    """
    Custom permission to only allow creating new users if not authenticated.
    For all other operations, user must be authenticated.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the account
        if view.action == 'destroy':
            return obj == request.user
        # For all other actions, only allow authenticated users
        return request.user and request.user.is_authenticated

