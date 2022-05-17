from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """Допуск для действий."""
    message = 'Недостаточно прав для совершения действия.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
