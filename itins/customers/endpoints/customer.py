from rest_framework import routers
from customers.api import CustomerViewSet

router = routers.DefaultRouter()
router.register('', CustomerViewSet, 'customer')

urlpatterns = router.urls
