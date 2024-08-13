from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from .models import Waypoint, Airport
from .serializers import WaypointSerializer, AirportSerializer




class LocationFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        airport_code = request.query_params.get('airport')
        hours = request.query_params.get('hours')
        travel_mode = request.query_params.get('travel_mode', 'driving')

        if airport_code and hours:
            try:
                airport = Airport.objects.get(iata_code=airport_code)
                hours = float(hours)
                
                if travel_mode == 'driving':
                    # Assume average speed of 60 km/h
                    distance = hours * 60
                elif travel_mode == 'flying':
                    # Assume average speed of 800 km/h
                    distance = hours * 800
                else:
                    return queryset

                return queryset.filter(location__distance_lte=(airport.location, D(km=distance)))
            except Airport.DoesNotExist:
                return queryset.none()

        return queryset

class WaypointViewSet(viewsets.ModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer
    filter_backends = (DjangoFilterBackend, LocationFilter)

class AirportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer