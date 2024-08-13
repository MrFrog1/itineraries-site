from rest_framework import serializers
from .models import Waypoint, Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'iata_code', 'location']

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = ['id', 'itinerary_day', 'agent_itinerary', 'hotel', 'component', 'itinerary_day_component', 'google_place_reference', 'place_name', 'description', 'ordering', 'location']