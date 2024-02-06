from rest_framework import routers
from db_changes.api import DbChangeViewSet

router = routers.DefaultRouter()
router.register('', DbChangeViewSet, 'db_change')

urlpatterns = router.urls
