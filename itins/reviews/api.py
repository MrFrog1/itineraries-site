from rest_framework import viewsets,filters
from.permissions import IsOwnerOrReadOnly
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['hotel__name', 'agent__name']  # Customize as needed


    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

