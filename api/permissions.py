from rest_framework import permissions

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
