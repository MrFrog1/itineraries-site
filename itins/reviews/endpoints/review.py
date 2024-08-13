from rest_framework.routers import DefaultRouter
from reviews.api import ReviewViewSet, ExternalReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'external-reviews', ExternalReviewViewSet)


urlpatterns = router.urls
