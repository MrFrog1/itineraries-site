from rest_framework import routers
from contacts.api import ContactViewSet

router = routers.DefaultRouter()
router.register('', ContactViewSet, 'contacts')

urlpatterns = router.urls
