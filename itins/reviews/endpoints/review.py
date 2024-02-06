from rest_framework import routers
from reviews.api import ReviewViewSet

router = routers.DefaultRouter()
router.register('', ReviewViewSet, 'reviews')

urlpatterns = router.urls
