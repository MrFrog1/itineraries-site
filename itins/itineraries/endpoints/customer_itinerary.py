from rest_framework import routers
from itineraries.api import CustomerItineraryViewSet

router = routers.DefaultRouter()
router.register('', CustomerItineraryViewSet, 'customer_itineraries')

urlpatterns = router.urls
