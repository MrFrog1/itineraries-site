from rest_framework import routers
from itineraries.api import ItineraryDayViewSet

router = routers.DefaultRouter()
router.register('', ItineraryDayViewSet, 'itinerary_days')

urlpatterns = router.urls
