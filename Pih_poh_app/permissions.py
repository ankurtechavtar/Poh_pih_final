# accounts/permissions.py

from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow full access to admins
    and restrict normal users to their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # If user is an admin (staff), grant full access
        if request.user.is_staff:
            return True
        # Otherwise, only allow if obj.id == request.user.id
        return obj.id == request.user.id
