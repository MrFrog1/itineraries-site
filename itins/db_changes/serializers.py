from rest_framework import serializers
from .models import DbChange

class DbChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbChange
        fields = ['user', 'timestamp', 'description']
        read_only_fields = ['user', 'timestamp', 'description']
