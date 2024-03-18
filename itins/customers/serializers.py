from rest_framework import serializers
from .models import User, AgentProfile, CustomerProfile, InterestCategory
from media.models import Photo, Video
from media.serializers import PhotoSerializer, VideoSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from reviews.models import Review  # Assuming you have a Review model that references User
from reviews.serializers import ReviewSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from hotels.models import Hotel
from hotels.serializers import HotelSerializer 
from itineraries.models import CustomerItinerary, AgentItinerary
from itineraries.serializers import AgentItinerarySerializer, CustomerItinerarySerializer

class UserSerializer(serializers.ModelSerializer):
    bio_photos = serializers.SerializerMethodField()
    bio_videos = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    hotels = serializers.SerializerMethodField()
    itineraries = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone_number', 'email', 'country','region', 'public_profile', 'nickname',
            'is_agent', 'is_customer', 'bio_photos', 'bio_videos', 'interests', 'reviews', 'hotels'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True},
            'email': {'read_only': True},
            # Potentially make other fields read-only as appropriate
        }

    def get_bio_photos(self, obj):
        # Assuming bio photos are relevant for agents
        if obj.is_agent:
            bio_photos = Photo.objects.filter(uploader=obj, is_agent_bio_photo=True)
            return PhotoSerializer(bio_photos, many=True, context=self.context).data
        return []

    def get_bio_videos(self, obj):
        # Assuming bio videos are relevant for agents
        if obj.is_agent:
            bio_videos = Video.objects.filter(uploader=obj, is_agent_bio_video=True)
            return VideoSerializer(bio_videos, many=True, context=self.context).data
        return []
    
    def get_interests(self, obj):
        # Check if the User instance has a linked CustomerProfile
        if hasattr(obj, 'customer_profile'):
            interests = obj.customer_profile.interests.all()
            return [interest.name for interest in interests]
        return []

    def get_reviews(self, obj):
        # Assuming Review model has a user field and a method to get visible reviews
        # This method should return serialized data for reviews linked to the user
        reviews = Review.objects.filter(customer=obj)  # Adjust query based on your model
        return ReviewSerializer(reviews, many=True, context=self.context).data  # Assuming you have a ReviewSerializer

    def get_hotels(self, obj):
        if obj.is_agent:
            hotels = Hotel.objects.filter(agent=obj)
            return HotelSerializer(hotels, many=True).data
        return []

    def get_itineraries(self, obj):
        if obj.is_agent:
            agent_itineraries = AgentItinerary.objects.filter(agent=obj)
            customer_itineraries = CustomerItinerary.objects.filter(original_itinerary__agent=obj)  # Ensure this is the correct relationship
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
        # Start with the base representation
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Remove fields that should not be included by default
        sensitive_fields = ['email', 'default_commission_percentage', 'default_organisation_fee', 'phone_number']
        for field in sensitive_fields:
            data.pop(field, None)

        # Visibility adjustments for agent users
        if instance.is_agent:
            if not instance.public_profile and (request.user.is_anonymous or request.user.is_customer):
                return {}  # Hide information for non-public agent profiles from anonymous and customer users
            # Adjust data or restrict fields as necessary for agent visibility
            return data  # Return modified or full data for agents

        # Visibility adjustments for customer users
        if instance.is_customer:
            # Initially restrict visibility for other customers
            if request.user.is_customer and request.user != instance:
                return {}  # Ensure customers cannot see other customers' information

            # Handle visibility for agents or the customer themselves
            if request.user.is_agent or request.user == instance:
                # Additional logic to handle agent-customer interaction or customer accessing their own data
                return data  # Modify this as per your specific requirements

            # Default case for admin or other roles
            return data

        # Fallback for any cases not explicitly handled above
        return data
        
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = list(UserSerializer.Meta.fields) + ['token',]  # Convert tuple to list and add 'token'

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def create(self, validated_data):
        # Use the existing logic from UserSerializer to handle user creation
        user = super().create(validated_data)
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims directly
        token['username'] = user.username
        token['is_agent'] = user.is_agent
        token['is_customer'] = user.is_customer
        return token

    def validate(self, attrs):
        # Authenticate user
        username_or_email = attrs.get('username')
        password = attrs.get('password')
        user = None

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(username=username_or_email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        # Authentication success
        data = super().validate(attrs)

        # Directly add necessary fields to the response
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_agent': user.is_agent,
            'is_customer': user.is_customer
            # Add other fields as necessary
        }

        # Only add itineraries and hotels if applicable
        if user.is_agent:
            agent_itineraries = AgentItinerary.objects.filter(agent=user)
            hotels = user.agentprofile.hotels.all()  # Adjust based on your model relations
            user_data['agent_itineraries'] = AgentItinerarySerializer(agent_itineraries, many=True).data
            user_data['hotels'] = HotelSerializer(hotels, many=True).data

        if user.is_customer:
            customer_itineraries = CustomerItinerary.objects.filter(customer=user)
            user_data['customer_itineraries'] = CustomerItinerarySerializer(customer_itineraries, many=True).data

        # Merge user data into token data
        data.update(user_data)

        return data
        
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

    def create(self, validated_data):
        interests_data = validated_data.pop('interests', [])  # Extract interests if provided
        validated_data['is_agent'] = False  # Ensure is_agent is set to False
        validated_data['is_customer'] = True  # Ensure is_customer is set to True
        
        user = User.objects.create_user(**validated_data)

        # Assign interests to the customer profile
        customer_profile = CustomerProfile.objects.get_or_create(user=user)[0]
        customer_profile.interests.set(interests_data)
        
        return user