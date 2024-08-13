from rest_framework import routers
from waypoints.api import AirportViewSet

router = routers.DefaultRouter()
router.register('', AirportViewSet, 'airports')

urlpatterns = router.urls