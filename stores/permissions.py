from rest_framework import permissions

from .models import Store, StoreStaff


def _get_store_from_view(view, obj=None):
    if obj is not None:
        if isinstance(obj, Store):
            return obj
        if hasattr(obj, "store"):
            return obj.store
    if hasattr(view, "get_store"):
        return view.get_store()
    return None


class IsStoreAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to everyone authenticated, but write access only to store admins.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        store = _get_store_from_view(view)
        if store:
            return self._is_store_admin(request.user, store)

        # For operations that aren't tied to a specific store yet (like create),
        # fall back to elevated role check (admin or librarian) when creating resources.
        action = getattr(view, "action", None)
        if action == "create":
            return (
                request.user
                and request.user.is_authenticated
                and getattr(request.user, "role", None) in ["admin", "librarian"]
            )

        # For other actions, defer the decision to the object permission once the store is known.
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        store = _get_store_from_view(view, obj)
        if store is None and isinstance(obj, Store):
            store = obj
        return self._is_store_admin(request.user, store)

    def _is_store_admin(self, user, store):
        if not user or not user.is_authenticated or store is None:
            return False
        if getattr(user, "role", None) == "admin":
            return True
        return StoreStaff.objects.filter(
            store=store, user=user, role=StoreStaff.ROLE_ADMIN
        ).exists()


class IsStoreStaffOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to authenticated users, but write access only to store staff.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        store = _get_store_from_view(view)
        return self._is_store_staff(request.user, store)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        store = _get_store_from_view(view, obj)
        if store is None and isinstance(obj, Store):
            store = obj
        return self._is_store_staff(request.user, store)

    def _is_store_staff(self, user, store):
        if not user or not user.is_authenticated or store is None:
            return False
        if getattr(user, "role", None) == "admin":
            return True
        return StoreStaff.objects.filter(store=store, user=user).exists()

