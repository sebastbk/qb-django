from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow the creator of an object to edit it.

    Assumes the model instance has a `created_by` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
