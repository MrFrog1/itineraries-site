from rest_framework import routers
from itineraries.api import ItineraryGroupingViewSet

router = routers.DefaultRouter()
router.register('', ItineraryGroupingViewSet, 'itinerary_groupings')

urlpatterns = router.urls
