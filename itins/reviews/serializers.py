from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['date_created', 'helpful_count', 'unhelpful_count', 'click_count']