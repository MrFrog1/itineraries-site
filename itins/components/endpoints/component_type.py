from rest_framework import routers
from components.api import ComponentTypeViewSet

router = routers.DefaultRouter()
router.register('', ComponentTypeViewSet, 'components')

urlpatterns = router.urls
