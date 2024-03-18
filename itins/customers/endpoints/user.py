from rest_framework import routers
from customers.api import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, 'user')

urlpatterns = router.urls
