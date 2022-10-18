from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwnerOrReadOnly(BasePermission):
    """Custom API permission to check if request user is the owner of the profile"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS) or (obj.user == request.user)
