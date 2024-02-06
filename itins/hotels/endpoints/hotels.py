from rest_framework import routers
from hotels.api import HotelViewSet

router = routers.DefaultRouter()
router.register('', HotelViewSet, 'hotels')

urlpatterns = router.urls
