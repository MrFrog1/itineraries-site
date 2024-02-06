from rest_framework import serializers
from .models import Waypoint

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = ['id', 'itinerary_day', 'agent_itinerary', 'component', 'itinerary_day_component', 'google_place_reference', 'place_name', 'description', 'ordering']
