from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

class ReadOnlyOrAdmin(BasePermission):
    """Allow read-only access to all, but write access only to admins."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
