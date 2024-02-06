from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAgentOrCustomerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj could be an instance of ItineraryDayComponent, ItineraryDay, or ItineraryGrouping
        # Check if the user is the agent or customer related to the object
        if hasattr(obj, 'customer_itinerary'):
            return obj.customer_itinerary.customer.user == request.user or obj.customer_itinerary.agent.user == request.user
        return False

    
class IsCustomerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the customer related to the CustomerItinerary
        return obj.customer.user == request.user
    
class IsAgentOwnerOrReadOnly(BasePermission):
    """
    Allows read-only access to anonymous users and write access to the agent owner.
    """
    def has_permission(self, request, view):
        # Allow read-only access for any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed for authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the agent owner
        return obj.agent.user == request.user

    # CHECK ALL THESE WHETHER THEY ACCURATELY REFLECT