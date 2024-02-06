from rest_framework import viewsets
from .models import ItineraryDayComponent, ItineraryDay, ItineraryGroup, ItineraryGrouping, CustomerItinerary, AgentItinerary
from .serializers import ItineraryDayComponentSerializer, ItineraryDaySerializer, ItineraryGroupSerializer, ItineraryGroupingSerializer, CustomerItinerarySerializer, AgentItinerarySerializer
from .permissions import IsAgentOrCustomerOwner, IsCustomerOwner, IsAgentOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly



class ItineraryDayComponentViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryDayComponentSerializer
    queryset = ItineraryDayComponent.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOrCustomerOwner()]
        return [IsAuthenticatedOrReadOnly()]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'agent'):
                return ItineraryDayComponent.objects.filter(itinerary_day__itinerary_group__agent_itinerary__agent=user.agent)
            elif hasattr(user, 'customer'):
                return ItineraryDayComponent.objects.filter(itinerary_day__itinerary_group__customer_itinerary__customer=user.customer)
        return ItineraryDayComponent.objects.none()
    


class ItineraryDayViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryDaySerializer
    queryset = ItineraryDay.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOrCustomerOwner()]
        return [IsAuthenticatedOrReadOnly()]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'agent'):
                return ItineraryDay.objects.filter(itinerary_group__agent_itinerary__agent=user.agent)
            elif hasattr(user, 'customer'):
                return ItineraryDay.objects.filter(itinerary_group__customer_itinerary__customer=user.customer)
        return ItineraryDay.objects.none()

class ItineraryGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryGroupSerializer
    queryset = ItineraryGroup.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'agent'):
                return ItineraryGroup.objects.filter(agent_itinerary__agent=user.agent)
            elif hasattr(user, 'customer'):
                return ItineraryGroup.objects.filter(customer_itinerary__customer=user.customer)
        return ItineraryGroup.objects.none()

class ItineraryGroupingViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryGroupingSerializer
    queryset = ItineraryGrouping.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOrCustomerOwner()]
        return [IsAuthenticatedOrReadOnly()]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'agent'):
                return ItineraryGrouping.objects.filter(agent_itinerary__agent=user.agent)
            elif hasattr(user, 'customer'):
                return ItineraryGrouping.objects.filter(customer_itinerary__customer=user.customer)
        return ItineraryGrouping.objects.none()
    

class CustomerItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerItinerarySerializer
    queryset = CustomerItinerary.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCustomerOwner()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'customer'):
            return CustomerItinerary.objects.filter(customer=user.customer)
        return CustomerItinerary.objects.none()


class AgentItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = AgentItinerarySerializer
    queryset = AgentItinerary.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
            user = self.request.user
            if user.is_authenticated and hasattr(user, 'agent'):
                return AgentItinerary.objects.filter(agent=user.agent)
            return AgentItinerary.objects.all()  # Visible to all users including anonymous