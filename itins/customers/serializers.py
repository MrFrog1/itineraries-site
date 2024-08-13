from rest_framework import serializers
from .models import User, AgentProfile, CustomerProfile, InterestCategory, ExpertiseCategory, PotentialAgent, UserAgent
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
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def flexible_url_validator(value):
    if value:
        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value
        try:
            URLValidator()(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid URL.")
    return value


class ExpertiseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseCategory
        fields = ['id', 'name']

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
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    public_profile = serializers.BooleanField(source='user.public_profile')
    agent_profile = serializers.SerializerMethodField()
    review_rating = serializers.SerializerMethodField()
    simple_itineraries = serializers.SerializerMethodField()
    detailed_itineraries = serializers.SerializerMethodField()
    website = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)
    instagram_link = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)

    class Meta:
        model = UserAgent
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'public_profile', 'password',
                  'short_bio', 'bio', 'business_name', 'website', 'instagram_link', 
                  'sustainability_practices', 'hotel_owner', 'default_commission_percentage', 
                  'default_organisation_fee', 'agent_profile', 'review_rating', 'simple_itineraries', 'detailed_itineraries']
        read_only_fields = ['review_rating', 'simple_itineraries', 'detailed_itineraries']
        extra_kwargs = {
            'short_bio': {'required': False},
            'bio': {'required': False},
            # Add other fields here that should be optional
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        is_agent = validated_data.pop('is_agent')

        user = User.objects.create_user(**user_data, password=password)
        user_agent = UserAgent.objects.create(user=user, **validated_data)
        return user_agent

    def get_agent_profile(self, obj):
        return {
            'bio': obj.bio,
            'expertise_categories': [cat.name for cat in obj.expertise_categories.all()],
            'business_name': obj.business_name,
            'website': obj.website,
            'instagram_link': obj.instagram_link,
            'sustainability_practices': obj.sustainability_practices,
            'hotel_owner': obj.hotel_owner,
            'accompanying_agent': obj.accompanying_agent.id if obj.accompanying_agent else None,
            'join_date': obj.join_date,
            'agent_starting_date': obj.agent_starting_date,
            'admin_description': obj.admin_description,
            'default_commission_percentage': obj.default_commission_percentage,
            'default_organisation_fee': obj.default_organisation_fee,
        }

    def get_review_rating(self, obj):
        reviews = Review.objects.filter(agent=obj.user)
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None

    def get_simple_itineraries(self, obj):
        if hasattr(obj.user, 'agent_itineraries'):
            return BasicAgentItinerarySerializer(obj.user.agent_itineraries.all(), many=True).data
        return []

    def get_detailed_itineraries(self, obj):
        if hasattr(obj.user, 'agent_itineraries'):
            return DetailedAgentItinerarySerializer(obj.user.agent_itineraries.all(), many=True).data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if isinstance(instance, User):
            instance = instance.user_agent

        if not instance.user.public_profile and (not request or not request.user.is_authenticated or request.user.is_customer):
            return {
                'id': instance.user.id,
                'username': instance.user.username,
                'public_profile': False
            }

        if not instance.user.public_profile and request.user.is_agent:
            return {
                'id': instance.user.id,
                'username': instance.user.username,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'public_profile': False,
                'review_rating': self.get_review_rating(instance)
            }

        if self.context.get('search_results', False):
            return {
                'id': instance.user.id,
                'username': instance.user.username,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'public_profile': True,
                'review_rating': self.get_review_rating(instance),
                'agent_profile': self.get_agent_profile(instance)
            }

        # If none of the above conditions are met, return the full representation
        data['username'] = instance.user.username
        data['email'] = instance.user.email
        data['first_name'] = instance.user.first_name
        data['last_name'] = instance.user.last_name
        data['public_profile'] = instance.user.public_profile
        return data

    
# class AllAgentsView(generics.ListAPIView):
#     serializer_class = AgentProfileSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         queryset = User.objects.filter(is_agent=True)

#         if not self.request.user.is_authenticated or self.request.user.is_customer:
#             queryset = queryset.filter(public_profile=True)

#         return queryset.select_related('agent_profile').prefetch_related('agent_profile__expertise_categories')

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         logger.info(f"Returning {len(serializer.data)} agents")
#         return Response(serializer.data)
    

class UserSerializer(serializers.ModelSerializer):
    bio_photos = serializers.SerializerMethodField()
    bio_videos = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    user_agent = AgentProfileSerializer(read_only=True)  # Changed from agent_profile to user_agent
    hotels = serializers.SerializerMethodField()
    itineraries = serializers.SerializerMethodField()
    is_visible = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone_number', 'email', 'country', 'region', 'public_profile', 'nickname',
            'is_agent', 'is_customer', 'is_superuser', 'bio_photos', 'bio_videos', 'interests', 'reviews', 
            'hotels', 'itineraries', 'user_agent', 'is_visible', 'is_blocked'
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
                user_agent = instance.user_agent
                ret['default_commission_percentage'] = user_agent.default_commission_percentage
                ret['default_organisation_fee'] = user_agent.default_organisation_fee
            else:
                ret.pop('phone_number', None)
                ret.pop('email', None)

        return ret
    


class PotentialAgentListSerializer(serializers.ModelSerializer):
    expertise_categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = PotentialAgent
        fields = ['id', 'first_name', 'last_name', 'email', 'business_name', 'expertise_categories']


class PotentialAgentSerializer(serializers.ModelSerializer):
    expertise_categories = serializers.PrimaryKeyRelatedField(queryset=ExpertiseCategory.objects.all(), many=True)

    class Meta:
        model = PotentialAgent
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'region', 
                  'short_bio', 'bio', 'business_name', 'website', 'instagram_link', 'expertise_categories', 'hotel_owner', 'admin_description']

    def create(self, validated_data):
        expertise_categories = validated_data.pop('expertise_categories', [])
        potential_agent = PotentialAgent.objects.create(**validated_data)
        potential_agent.expertise_categories.set(expertise_categories)
        return potential_agent

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