from rest_framework import viewsets
from .models import Hotel, CustomizedHotel, AgentHotel, HotelRoom, RoomPrice
from .serializers import HotelSerializer, CustomizedHotelSerializer, AgentHotelSerializer, HotelRoomSerializer, RoomPriceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsHotelOwnerPermission, IsRoomPriceOwner, IsAgentHotelOwner

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class CustomizedHotelViewSet(viewsets.ModelViewSet):
    queryset = CustomizedHotel.objects.all()
    serializer_class = CustomizedHotelSerializer

# These two functions just ensure that the request is passed to the serializer, so that we can exclude the private_info or any fields that we dont want anyone but the hotel owner to see

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomizedHotelSerializer
        # Define other serializer classes for different actions if needed

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser | IsHotelOwnerPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
class AgentHotelViewSet(viewsets.ModelViewSet):
    serializer_class = AgentHotelSerializer
    permission_classes = [IsAuthenticated, IsAgentHotelOwner]  # Use the custom permission here


    def get_queryset(self):
        return AgentHotel.objects.filter(agent=self.request.user.agent)
    
class HotelRoomViewSet(viewsets.ModelViewSet):
    serializer_class = HotelRoomSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'hotel_owner'):
            # Return rooms associated with CustomizedHotel for this hotel owner
            return HotelRoom.objects.filter(customized_hotel__hotel_owner=user.hotel_owner)
        elif hasattr(user, 'agent'):

            # Return rooms associated with AgentHotel for this agent
            return HotelRoom.objects.filter(agent_hotel__agent=user.agent)

        else:
            # Return a general queryset or none
            return HotelRoom.objects.none()

class RoomPriceViewSet(viewsets.ModelViewSet):
    queryset = RoomPrice.objects.all()
    serializer_class = RoomPriceSerializer
    permission_classes = [IsAuthenticated, IsRoomPriceOwner]  # Add the custom permission class here
