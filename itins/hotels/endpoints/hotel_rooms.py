from rest_framework import routers
from hotels.api import HotelRoomViewSet

router = routers.DefaultRouter()
router.register('', HotelRoomViewSet, 'hotel_rooms')

urlpatterns = router.urls
