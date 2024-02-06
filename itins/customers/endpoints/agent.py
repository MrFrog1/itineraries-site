from rest_framework import routers
from customers.api import AgentViewSet

router = routers.DefaultRouter()
router.register('', AgentViewSet, 'agent')

urlpatterns = router.urls
