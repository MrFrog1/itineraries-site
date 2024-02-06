from rest_framework import routers
from itineraries.api import ItineraryDayComponentViewSet

router = routers.DefaultRouter()
router.register('', ItineraryDayComponentViewSet, 'itinerary_day_components')

urlpatterns = router.urls
