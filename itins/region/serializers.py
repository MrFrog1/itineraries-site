from rest_framework import serializers
from .models import Region, RegionSubsection
from media.models import Photo
from media.serializers import BasicPhotoSerializer, DetailedPhotoSerializer


class BasicRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'description', 'shortkey', 'best_months', 'best_for']


class DetailedRegionSerializer(serializers.ModelSerializer):
    basic_photos = serializers.SerializerMethodField()
    detailed_photos = serializers.SerializerMethodField()
 
    class Meta:
        model = Region
        fields = [
            'id', 'name', 'description', 'shortkey', 'best_months', 'best_for',
            'january_min_temperature', 'january_max_temperature',
            'february_min_temperature', 'february_max_temperature',
            'march_min_temperature', 'march_max_temperature',
            'april_min_temperature', 'april_max_temperature',
            'may_min_temperature', 'may_max_temperature',
            'june_min_temperature', 'june_max_temperature',
            'july_min_temperature', 'july_max_temperature',
            'august_min_temperature', 'august_max_temperature',
            'september_min_temperature', 'september_max_temperature',
            'october_min_temperature', 'october_max_temperature',
            'november_min_temperature', 'november_max_temperature',
            'december_min_temperature', 'december_max_temperature',
            'january_weather', 'february_weather', 'march_weather',
            'april_weather', 'may_weather', 'june_weather',
            'july_weather', 'august_weather', 'september_weather',
            'october_weather', 'november_weather', 'december_weather',
            'basic_photos', 'detailed_photos'
        ]

    def get_basic_photos(self, obj):
        photos = Photo.objects.filter(region=obj)
        return BasicPhotoSerializer(photos, many=True).data

    def get_detailed_photos(self, obj):
        photos = Photo.objects.filter(region=obj)
        return DetailedPhotoSerializer(photos, many=True).data
    
class RegionSubsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionSubsection
        fields = ['all']