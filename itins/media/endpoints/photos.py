from rest_framework import routers
from media.api import PhotoViewSet

router = routers.DefaultRouter()
router.register('', PhotoViewSet, 'photo')

urlpatterns = router.urls
