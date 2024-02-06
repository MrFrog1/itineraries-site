from rest_framework import routers
from hotels.api import RoomPriceViewSet

router = routers.DefaultRouter()
router.register('', RoomPriceViewSet, 'room_prices')

urlpatterns = router.urls
