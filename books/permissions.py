from rest_framework import permissions

class RoleBasedAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == 'admin':
            return True

        if request.user.role == 'editor' and request.method in ['POST', 'PUT', 'PATCH']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'editor' and obj.owner == request.user:
            return request.method in ['GET', 'PUT', 'PATCH']
        return request.method in permissions.SAFE_METHODS
