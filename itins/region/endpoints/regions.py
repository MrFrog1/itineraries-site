from rest_framework import routers
from region.api import RegionViewSet

router = routers.DefaultRouter()
router.register('', RegionViewSet, 'regions')

urlpatterns = router.urls