from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

class IsHotelOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.hotel_owner.user == request.user or request.user.is_superuser

class IsAgentHotelOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.agent == request.user.agent or request.user.is_superuser

class IsHotelRoomOwnerOrAgentOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.customized_hotel:
            return obj.customized_hotel.hotel_owner.user == request.user or request.user.is_superuser
        if obj.agent_hotel:
            return obj.agent_hotel.agent == request.user.agent or request.user.is_superuser
        return False

class IsRoomPriceOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.hotel_room.agent_hotel:
            return obj.hotel_room.agent_hotel.agent == request.user.agent or request.user.is_superuser
        if obj.hotel_room.customized_hotel:
            return obj.hotel_room.customized_hotel.hotel_owner.user == request.user or request.user.is_superuser
        return False
    

# class IsHotelOwnerPermission(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of a hotel to edit it.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Assuming 'obj' is a CustomizedHotel instance
#         # Check if the user is the owner of the hotel
#         return obj.hotel_owner.user == request.user
    
# class IsRoomPriceOwner(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of a RoomPrice to edit it.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Check if the RoomPrice is associated with an AgentHotel and if the user is the agent
#         if obj.hotel_room.agent_hotel:
#             return obj.hotel_room.agent_hotel.agent == request.user.agent

#         # Check if the RoomPrice is associated with a CustomizedHotel and if the user is the hotel owner
#         if obj.hotel_room.customized_hotel:
#             return obj.hotel_room.customized_hotel.hotel_owner == request.user.agent

#         # If neither, deny permission
#         return False
    
# class IsAgentHotelOwner(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an AgentHotel to edit it.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Check if the user is the owner of the agent hotel
#         return obj.agent == request.user.agent
    

# class IsHotelRoomOwnerOrAgent(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Check if user is the owner of a CustomizedHotel room
#         if obj.customized_hotel and obj.customized_hotel.hotel_owner == request.user.hotel_owner:
# # PERHAPS THIS user.hotel_owner isnt correct? Could be just user.agent?
#             return True

#         # Check if user is the agent of an AgentHotel room
#         if obj.agent_hotel and obj.agent_hotel.agent == request.user.agent:
#             return True

#         return False