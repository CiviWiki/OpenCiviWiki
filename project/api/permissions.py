from rest_framework.permissions import BasePermission, SAFE_METHODS
from .utils import get_account


class IsOwnerOrReadOnly(BasePermission):
    """ Custom API permission to check if request user is the owner of the model """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS) or (
            obj.author == get_account(user=request.user)
        )


class IsProfileOwnerOrReadOnly(BasePermission):
    """ Custom API permission to check if request user is the owner of the account """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS) or (obj.user == request.user)


class IsProfileOwnerOrDuringRegistrationOrReadOnly(IsProfileOwnerOrReadOnly):
    """ """
    def has_object_permission(self, request, view, obj):
        if obj.full_account:
            return super(
                IsProfileOwnerOrDuringRegistrationOrReadOnly, self
            ).has_object_permission(request, view, obj)
        return True
