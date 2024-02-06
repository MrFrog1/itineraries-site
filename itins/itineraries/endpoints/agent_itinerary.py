from rest_framework import routers
from itineraries.api import AgentItineraryViewSet

router = routers.DefaultRouter()
router.register('', AgentItineraryViewSet, 'agent_itineraries')

urlpatterns = router.urls
