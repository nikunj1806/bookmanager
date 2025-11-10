from rest_framework import permissions

class IsAdminOrLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in (request.user.ROLE_LIBRARIAN, request.user.ROLE_ADMIN)

class IsOwnerOrLibrarianOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods to everyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role == request.user.ROLE_ADMIN or request.user.role == request.user.ROLE_LIBRARIAN:
            return True
        # members can act on their own records (e.g., their loans)
        return getattr(obj, 'member', None) == request.user
