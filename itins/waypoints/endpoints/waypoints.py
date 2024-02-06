from rest_framework import routers
from waypoints.api import WaypointViewSet

router = routers.DefaultRouter()
router.register('', WaypointViewSet, 'waypoints')

urlpatterns = router.urls
