from rest_framework import routers
from contacts.api import ContactCategoryViewSet

router = routers.DefaultRouter()
router.register('', ContactCategoryViewSet, 'contact_categories')

urlpatterns = router.urls
