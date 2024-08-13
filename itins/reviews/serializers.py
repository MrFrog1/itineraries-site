from rest_framework import serializers
from .models import Review, ExternalReview, ExternalReviewSource

class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['date_created', 'helpful_count', 'unhelpful_count', 'click_count']

class ExternalReviewSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalReviewSource
        fields = ['id', 'name', 'weight']

class ExternalReviewSerializer(serializers.ModelSerializer):
    source = ExternalReviewSourceSerializer(read_only=True)

    class Meta:
        model = ExternalReview
        fields = ['id', 'hotel', 'source', 'rating', 'review_count', 'last_updated']
        read_only_fields = ['last_updated']
