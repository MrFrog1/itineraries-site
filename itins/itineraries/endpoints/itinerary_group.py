from rest_framework import routers
from itineraries.api import ItineraryGroupViewSet

router = routers.DefaultRouter()
router.register('', ItineraryGroupViewSet, 'itinerary_groups')

urlpatterns = router.urls
