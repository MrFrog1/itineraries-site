from rest_framework import viewsets
from .models import Waypoint
from .serializers import WaypointSerializer

class WaypointViewSet(viewsets.ModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer

    # You can add custom methods or override existing ones if needed