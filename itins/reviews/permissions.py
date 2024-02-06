from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """Allow read-only access to all, but write access only to the owner."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customer.user == request.user