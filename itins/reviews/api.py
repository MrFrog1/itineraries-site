
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from .models import Review, ExternalReview
from .serializers import ReviewSerializer, ExternalReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['hotel__name', 'agent__username']  # Adjusted 'agent__name' to 'agent__username'

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ExternalReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExternalReview.objects.all()
    serializer_class = ExternalReviewSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['hotel__name', 'source__name']

    def get_queryset(self):
        return ExternalReview.objects.select_related('source', 'hotel')