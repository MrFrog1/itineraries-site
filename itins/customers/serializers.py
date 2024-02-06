from rest_framework import serializers
from .models import Agent, Customer
from media.serializers import PhotoSerializer, VideoSerializer
from media.models import Photo, Video
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AgentSerializer(serializers.ModelSerializer):
    bio_photos = serializers.SerializerMethodField()
    bio_videos = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            'user', 'phone_number', 'email_address', 'region', 'bio',
            'expertise_category', 'hotel_owner', 'paired_with_other_agent',
            'join_date', 'nickname', 'default_commission_percentage',
            'default_organisation_fee', 'bio_photos', 'bio_videos'
        ]
        read_only_fields = [
            'default_commission_percentage', 'default_organisation_fee'
        ]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # If the request user is not the agent, hide certain fields
        if request and request.user != instance.user:
            hide_fields = ['default_commission_percentage', 'default_organisation_fee']
            for field in hide_fields:
                representation.pop(field, None)

        return representation

    def get_bio_photos(self, obj):
        bio_photos = Photo.objects.filter(uploader=obj.user, is_agent_bio_photo=True)
        return PhotoSerializer(bio_photos, many=True).data

    def get_bio_videos(self, obj):
        bio_videos = Video.objects.filter(uploader=obj.user, is_agent_bio_video=True)
        return VideoSerializer(bio_videos, many=True).data
 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'phone_number', 'email_address', 'location', 'region', 'interests']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Check if the request is from the customer themselves
        if request and hasattr(request.user, 'customer') and request.user.customer == instance:
            # Customer can view all their own data
            return representation

        # Logic for a public profile
        if instance.public_profile:
            public_fields = ['nickname', 'location']  # Fields visible to everyone if public profile is opted
            return {field: representation[field] for field in public_fields}

        # Logic for agent viewing customer data
        if hasattr(request.user, 'agent'):
            if instance.is_agent_blocked(request.user.agent):
                return {}  # Return empty data if blocked

            if not instance.has_interacted_with(request.user.agent):
                return {}  # Restrict data if no interaction

        # Hide all data if not a public profile and the user is not the customer themselves
        return {}
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims...
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user