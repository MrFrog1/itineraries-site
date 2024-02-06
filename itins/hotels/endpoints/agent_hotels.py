from rest_framework import routers
from hotels.api import AgentHotelViewSet

router = routers.DefaultRouter()
router.register('', AgentHotelViewSet, 'agent_hotels')

urlpatterns = router.urls
