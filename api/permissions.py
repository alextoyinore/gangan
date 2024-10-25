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
        # if view.action == 'list':
        #     if request.user.is_superuser:
        #         return True
        #     return False
        # For all other actions, only allow authenticated users
        return request.user and request.user.is_authenticated


class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        token = Token.objects.get(user=request.user)
        if token is not None:
            return True
        return False

    