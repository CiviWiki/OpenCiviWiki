from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Custom API permission to check if request user is the owner of the model"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS) or (obj.author == request.user)
