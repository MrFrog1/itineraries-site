from rest_framework import routers
from hotels.api import CustomizedHotelViewSet

router = routers.DefaultRouter()
router.register('', CustomizedHotelViewSet, 'customized_hotels')
urlpatterns = router.urls
