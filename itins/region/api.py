from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ReadOnlyOrAdmin
from .serializers import BasicRegionSerializer, DetailedRegionSerializer
from .models import Region, RegionSubsection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import django_filters

class RegionFilter(django_filters.FilterSet):
    best_months = django_filters.CharFilter(method='filter_best_months')
    best_for = django_filters.CharFilter(method='filter_best_for')

    class Meta:
        model = Region
        fields = ['best_months', 'best_for']

    def filter_best_months(self, queryset, name, value):
        return queryset.filter(best_months__contains=[value])

    def filter_best_for(self, queryset, name, value):
        return queryset.filter(best_for__contains=[value])

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [ReadOnlyOrAdmin]

    filterset_class = RegionFilter
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicRegionSerializer
        return DetailedRegionSerializer
    
    def get_permissions(self):
        if self.action == 'detailed':
            return [AllowAny()]
        return [ReadOnlyOrAdmin()]

    @action(detail=False, methods=['post'])
    def detailed(self, request):
        ids = request.data.get('ids', [])
        regions = Region.objects.filter(id__in=ids)
        serializer = DetailedRegionSerializer(regions, many=True)
        return Response(serializer.data)
    
class RegionSubsectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegionSubsection.objects.all()
    permission_classes = [ReadOnlyOrAdmin]
