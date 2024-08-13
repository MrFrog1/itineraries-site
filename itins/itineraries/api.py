from rest_framework import viewsets, filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as django_filters
from .models import (
    ItineraryDayComponent, ItineraryDay, ItineraryGroup, 
    ItineraryGrouping, CustomerItinerary, AgentItinerary
)
from .serializers import (
    BasicAgentItinerarySerializer, DetailedAgentItinerarySerializer,
    ItineraryDayComponentSerializer, ItineraryDaySerializer,
    ItineraryGroupSerializer, ItineraryGroupingSerializer,
    CustomerItinerarySerializer
)
from .permissions import IsAgentOrCustomerOwner, IsCustomerOwner, IsAgentOwnerOrReadOnly


class AgentItineraryFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="cost_for_1_pax", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="cost_for_1_pax", lookup_expr='lte')
    regions = django_filters.CharFilter(method='filter_regions')
    types = django_filters.CharFilter(method='filter_types')
    tags = django_filters.CharFilter(method='filter_tags')


    class Meta:
        model = AgentItinerary
        fields = ['min_price', 'max_price', 'regions', 'types', 'tags']

    def filter_regions(self, queryset, name, value):
        region_ids = value.split(',')
        return queryset.filter(region__id__in=region_ids)

    def filter_types(self, queryset, name, value):
        types = value.split(',')
        return queryset.filter(type__in=types)

    def filter_tags(self, queryset, name, value):
        tag_names = value.split(',')
        return queryset.filter(tags__name__in=tag_names)

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
    queryset = AgentItinerary.objects.all()
    filter_backends = (django_filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter)
    filterset_class = AgentItineraryFilter
    search_fields = ['name', 'description', 'region__name', 'category']
    ordering_fields = ['name', 'cost_for_1_pax', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgentOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'agent'):
            return AgentItinerary.objects.filter(agent=user.agent)
        return AgentItinerary.objects.all()  # Visible to all users including anonymous
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BasicAgentItinerarySerializer
        return DetailedAgentItinerarySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['post'])
    def detailed(self, request):
        ids = request.data.get('ids', [])
        itineraries = AgentItinerary.objects.filter(id__in=ids)
        serializer = DetailedAgentItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)    