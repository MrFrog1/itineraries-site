from rest_framework import routers
from components.api import ComponentViewSet

router = routers.DefaultRouter()
router.register('', ComponentViewSet, 'components')

urlpatterns = router.urls
