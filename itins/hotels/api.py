from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Hotel, CustomizedHotel, AgentHotel, HotelRoom, RoomPrice
from .serializers import BasicHotelSerializer, DetailedHotelSerializer,  CustomizedHotelSerializer, AgentHotelSerializer, HotelRoomSerializer, RoomPriceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly, IsHotelOwnerOrReadOnly, IsAgentHotelOwnerOrReadOnly, IsHotelRoomOwnerOrAgentOrReadOnly, IsRoomPriceOwnerOrReadOnly
from django_filters import rest_framework as filters

class HotelFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="min_price_in_INR", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="min_price_in_INR", lookup_expr='lte')
    region = filters.CharFilter(field_name="region__name", lookup_expr='icontains')
    type = filters.CharFilter(field_name="type", lookup_expr='iexact')
    tags = filters.CharFilter(method='filter_tags')
    
    class Meta:
        model = Hotel
        fields = ['min_price', 'max_price', 'region', 'type', 'tags']

    def filter_regions(self, queryset, name, value):
        region_ids = value.split(',')
        return queryset.filter(region__id__in=region_ids)

    def filter_types(self, queryset, name, value):
        types = value.split(',')
        return queryset.filter(type__in=types)


    def filter_tags(self, queryset, name, value):
        tag_names = value.split(',')
        return queryset.filter(tags__name__in=tag_names)
    


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HotelFilter
    search_fields = ['name', 'description', 'region__name', 'type']
    ordering_fields = ['name', 'min_price_in_INR', 'rating']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicHotelSerializer
        return DetailedHotelSerializer


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def detailed(self, request):
        ids = request.data.get('ids', [])
        hotels = Hotel.objects.filter(id__in=ids)
        serializer = DetailedHotelSerializer(hotels, many=True)
        return Response(serializer.data)
    

class CustomizedHotelViewSet(viewsets.ModelViewSet):
    queryset = CustomizedHotel.objects.all()
    serializer_class = CustomizedHotelSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]

# These two functions just ensure that the request is passed to the serializer, so that we can exclude the private_info or any fields that we dont want anyone but the hotel owner to see

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomizedHotel.objects.all()
        return CustomizedHotel.objects.filter(hotel_owner__user=user)


    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomizedHotelSerializer
        # For all other actions, including 'create', use the default serializer
        return CustomizedHotelSerializer

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_superuser:
            # Remove fields that hotel owners are not allowed to edit
            for field in ['name', 'description', 'platform_hotel', 'region', 'min_price_in_INR', 'is_active']:
                serializer.validated_data.pop(field, None)

        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        print('serializer trying to save')
        # if self.request.user.is_superuser:
        #     print('serializer trying to save')
        #     serializer.save()
        # else:
        #     raise PermissionDenied("Only admin users can create CustomizedHotels.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AgentHotelViewSet(viewsets.ModelViewSet):
    serializer_class = AgentHotelSerializer
    permission_classes = [IsAgentHotelOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AgentHotel.objects.all()
        return AgentHotel.objects.filter(agent=user.agent)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent)

class HotelRoomViewSet(viewsets.ModelViewSet):
    serializer_class = HotelRoomSerializer
    permission_classes = [IsHotelRoomOwnerOrAgentOrReadOnly]

    def get_queryset(self):
        return HotelRoom.objects.all()


    # def get_queryset(self):
    #     user = self.request.user
    #     if hasattr(user, 'hotel_owner'):
    #         # Return rooms associated with CustomizedHotel for this hotel owner
    #         return HotelRoom.objects.filter(customized_hotel__hotel_owner=user.hotel_owner)
    #     elif hasattr(user, 'agent'):

    #         # Return rooms associated with AgentHotel for this agent
    #         return HotelRoom.objects.filter(agent_hotel__agent=user.agent)

    #     else:
    #         # Return a general queryset or none
    #         return HotelRoom.objects.none()

class RoomPriceViewSet(viewsets.ModelViewSet):
    queryset = RoomPrice.objects.all()
    serializer_class = RoomPriceSerializer
    permission_classes = [IsRoomPriceOwnerOrReadOnly]
