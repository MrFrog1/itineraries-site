from rest_framework import routers
from media.api import VideoViewSet

router = routers.DefaultRouter()
router.register('', VideoViewSet, 'video')

urlpatterns = router.urls
