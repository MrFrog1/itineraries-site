from rest_framework import routers
from contacts.api import ContactBusinessViewSet

router = routers.DefaultRouter()
router.register('', ContactBusinessViewSet, 'contact_businesses')

urlpatterns = router.urls
