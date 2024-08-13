from rest_framework import serializers
from .models import User, AgentProfile, CustomerProfile, InterestCategory
from media.models import Photo, Video
from media.serializers import DetailedPhotoSerializer, VideoSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from hotels.models import AgentHotel
from hotels.serializers import AgentHotelSerializer 
from itineraries.models import CustomerItinerary, AgentItinerary
from itineraries.serializers import BasicAgentItinerarySerializer, DetailedAgentItinerarySerializer, CustomerItinerarySerializer
from oauth2_provider.models import Application
from django.db.models import Avg
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'is_superuser', 'is_agent', 'is_customer', 'region']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'customer_profile'):
            data['interests'] = [interest.name for interest in instance.customer_profile.interests.all()]
        return data
    

class AgentProfileSerializer(serializers.ModelSerializer):
    agent_profile = serializers.SerializerMethodField()
    review_rating = serializers.SerializerMethodField()
    simple_itineraries = serializers.SerializerMethodField()
    detailed_itineraries = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'public_profile', 
                  'agent_profile', 'review_rating', 'simple_itineraries', 'detailed_itineraries']

    def get_agent_profile(self, obj):
        if hasattr(obj, 'agent_profile'):
            profile = obj.agent_profile
            return {
                'bio': profile.bio,
                'expertise_categories': [cat.name for cat in profile.expertise_categories.all()],
                'business_name': profile.business_name,
                'website': profile.website,
                'instagram_link': profile.instagram_link,
                'sustainability_practices': profile.sustainability_practices,
            }
        return None

    def get_review_rating(self, obj):
        reviews = Review.objects.filter(agent=obj)
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None

    def get_simple_itineraries(self, obj):
        if hasattr(obj, 'agent_itineraries'):
            return BasicAgentItinerarySerializer(obj.agent_itineraries.all(), many=True).data
        return []

    def get_detailed_itineraries(self, obj):
        if hasattr(obj, 'agent_itineraries'):
            return DetailedAgentItinerarySerializer(obj.agent_itineraries.all(), many=True).data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not instance.public_profile and (not request or not request.user.is_authenticated or request.user.is_customer):
            # If the profile is not public and the requester is not authenticated or is a customer,
            # only return minimal information
            return {
                'id': instance.id,
                'username': instance.username,
                'public_profile': False
            }

        if not instance.public_profile and request.user.is_agent:
            # If the requester is an agent, return slightly more information
            return {
                'id': instance.id,
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'public_profile': False,
                'review_rating': data['review_rating']
            }

        # For public profiles or admin users, determine what to show based on the context
        if self.context.get('search_results', False):
            # If this is for search results, return a subset of fields
            return {
                'id': instance.id,
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'public_profile': True,
                'review_rating': data['review_rating'],
                'agent_profile': {
                    'business_name': data['agent_profile']['business_name'] if data['agent_profile'] else None,
                    'expertise_categories': data['agent_profile']['expertise_categories'] if data['agent_profile'] else []
                }
            }

        # For detailed view (not search results), return all fields
        return data
    
class AllAgentsView(generics.ListAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = User.objects.filter(is_agent=True)

        if not self.request.user.is_authenticated or self.request.user.is_customer:
            queryset = queryset.filter(public_profile=True)

        return queryset.select_related('agent_profile').prefetch_related('agent_profile__expertise_categories')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Returning {len(serializer.data)} agents")
        return Response(serializer.data)
    
class UserSerializer(serializers.ModelSerializer):
    bio_photos = serializers.SerializerMethodField()
    bio_videos = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    agent_profile = AgentProfileSerializer(read_only=True)
    hotels = serializers.SerializerMethodField()
    itineraries = serializers.SerializerMethodField()
    is_visible = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone_number', 'email', 'country', 'region', 'public_profile', 'nickname',
            'is_agent', 'is_customer', 'is_superuser', 'bio_photos', 'bio_videos', 'interests', 'reviews', 
            'hotels', 'itineraries', 'agent_profile', 'is_visible', 'is_blocked'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True},
            'email': {'read_only': True},
        }

    def get_is_visible(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return obj.public_profile
        if request.user.is_superuser or request.user == obj:
            return True
        if obj.public_profile:
            return True
        if request.user.is_agent and obj.is_customer:
            return obj.has_interacted_with(request.user) and not obj.customer_profile.is_agent_blocked(request.user)
        return False

    def get_is_blocked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated or not request.user.is_agent:
            return False
        if obj.is_customer:
            return obj.customer_profile.is_agent_blocked(request.user)
        return False
    
    def get_bio_photos(self, obj):
        if obj.is_agent:
            bio_photos = Photo.objects.filter(uploader=obj, is_agent_bio_photo=True)
            return DetailedPhotoSerializer(bio_photos, many=True, context=self.context).data
        return []

    def get_bio_videos(self, obj):
        if obj.is_agent:
            bio_videos = Video.objects.filter(uploader=obj, is_agent_bio_video=True)
            return VideoSerializer(bio_videos, many=True, context=self.context).data
        return []
    
    def get_interests(self, obj):
        if hasattr(obj, 'customer_profile'):
            interests = obj.customer_profile.interests.all()
            return [interest.name for interest in interests]
        return []

    def get_reviews(self, obj):
        reviews = Review.objects.filter(customer=obj)
        return ReviewSerializer(reviews, many=True, context=self.context).data

    def get_hotels(self, obj):
        if obj.is_agent:
            hotels = AgentHotel.objects.filter(agent=obj)
            return AgentHotelSerializer(hotels, many=True).data
        return []

    def get_itineraries(self, obj):
        if obj.is_agent:
            agent_itineraries = AgentItinerary.objects.filter(agent=obj)
            customer_itineraries = CustomerItinerary.objects.filter(original_itinerary__agent=obj)
            return {
                'agent_itineraries': AgentItinerarySerializer(agent_itineraries, many=True, context={'request': self.context.get('request')}).data,
                'customer_itineraries': CustomerItinerarySerializer(customer_itineraries, many=True, context={'request': self.context.get('request')}).data
            }
        if obj.is_customer:
            customer_itineraries = CustomerItinerary.objects.filter(customer=obj)
            return {
                'customer_itineraries': CustomerItinerarySerializer(customer_itineraries, many=True, context={'request': self.context.get('request')}).data
            }
        return {}
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        is_visible = self.get_is_visible(instance)
        is_blocked = self.get_is_blocked(instance)

        if not is_visible:
            return {'id': instance.id, 'is_visible': False, 'is_blocked': is_blocked}

        if instance.is_customer and not instance.public_profile:
            if request and request.user.is_agent and is_visible and not is_blocked:
                visible_fields = ['id', 'username', 'nickname', 'country', 'region', 'is_customer', 'is_visible', 'is_blocked']
                ret = {k: v for k, v in ret.items() if k in visible_fields}
            else:
                return {'id': instance.id, 'is_visible': False, 'is_blocked': is_blocked}

        if instance.is_agent:
            if request and request.user.is_authenticated and (request.user.is_superuser or request.user == instance):
                agent_profile = instance.agent_profile
                ret['default_commission_percentage'] = agent_profile.default_commission_percentage
                ret['default_organisation_fee'] = agent_profile.default_organisation_fee
            else:
                ret.pop('phone_number', None)
                ret.pop('email', None)

        return ret
    
class CustomerRegisterSerializer(serializers.ModelSerializer):
    interests = serializers.SlugRelatedField(
        slug_field='name',
        queryset=InterestCategory.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'country', 'region', 'is_agent', 'is_customer', 'interests']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Only admin users can set is_agent to True
        if data.get('is_agent') and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("Only admin users can create agent accounts.")
        return data
    
    def create(self, validated_data):
        interests_data = validated_data.pop('interests', [])
        validated_data['is_agent'] = False
        validated_data['is_customer'] = True
        
        validated_data['is_customer'] = not validated_data.get('is_agent', False)
        
        user = User.objects.create_user(**validated_data)

        if user.is_customer:
            customer_profile = CustomerProfile.objects.get_or_create(user=user)[0]
            customer_profile.interests.set(interests_data)
        elif user.is_agent:
            AgentProfile.objects.get_or_create(user=user)

        # Create OAuth2 application for the user
        Application.objects.create(
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            name=f"{user.username}'s application"
        )
        
        return user
    


class AgentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'country', 'region', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        AgentProfile.objects.create(user=user)
        return user