from rest_framework import viewsets, filters
from .permissions import ReadOnlyOrAdmin
from .serializers import RegionSerializer
from .models import Region

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [ReadOnlyOrAdmin]  # Assuming ReadOnlyOrAdmin is your custom permission class

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'january_weather', 'july_weather']  # Customize as needed
    ordering_fields = ['description', 'january_weather', 'july_weather']  # Customize as needed