from rest_framework import serializers
from .models import Hotel, CustomizedHotel, PaymentType, AgentHotel, HotelRoom, RoomPrice, HotelActivities, HotelAmenities, HotelInfo
from common.serializers import  TagSerializer
from common.models import Tag
from reviews.serializers import ExternalReviewSerializer
# from common.email_validator import FlexibleURLField
# These use CustomizedHotel as a default - as these are the ones on the platform. Once the apop matures into adding random hotels that
# dont have information, then we can add different ones that use just the Hotel model
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def flexible_url_validator(value):
    if value:
        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value
        try:
            URLValidator()(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid URL.")
    return value


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'payment_type']  # Adjust fields as needed



class BasicHotelSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    overall_rating = serializers.FloatField(read_only=True)
    is_customized = serializers.SerializerMethodField()
    hotel_owner = serializers.SerializerMethodField()
    hotel_owner_role = serializers.SerializerMethodField()
    pet_friendly = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'region', 'type', 'tags', 'min_price_in_INR', 'is_active', 'overall_rating', 'is_customized', 'hotel_owner', 'hotel_owner_role', 'pet_friendly']

    def get_is_customized(self, obj):
        return hasattr(obj, 'customizedhotel')

    def get_hotel_owner(self, obj):
        if hasattr(obj, 'customizedhotel'):
            return obj.customizedhotel.hotel_owner.id
        return None

    def get_hotel_owner_role(self, obj):
        if hasattr(obj, 'customizedhotel'):
            return obj.customizedhotel.hotel_owner_role
        return None

    def get_pet_friendly(self, obj):
        if hasattr(obj, 'customizedhotel'):
            return obj.customizedhotel.pet_friendly
        return None
    
    
class DetailedHotelSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    external_reviews = ExternalReviewSerializer(many=True, read_only=True)
    overall_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = CustomizedHotel
        fields = '__all__'


class HotelActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelActivities
        fields = '__all__'

class HotelAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenities
        fields = '__all__'

class HotelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInfo
        fields = '__all__'



class RoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrice
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        is_owner = (request and (request.user.is_superuser or 
                                 (instance.hotel_room.agent_hotel and request.user == instance.hotel_room.agent_hotel.agent) or 
                                 (instance.hotel_room.customized_hotel and request.user == instance.hotel_room.customized_hotel.hotel_owner.user)))
        if not is_owner:
            for field in ['rack_price_1p', 'rack_price_2p', 'rack_price_3p', 'rack_price_2p_child', 'rack_price_4p', 'rack_price_3p_child', 'rack_price_4p_child',
                          'overridden_net_price_1p', 'overridden_net_price_2p', 'overridden_net_price_3p', 'overridden_net_price_2p_child', 'overridden_net_price_4p', 'overridden_net_price_3p_child', 'overridden_net_price_4p_child']:
                data.pop(field, None)
        return data
    
    

class HotelRoomSerializer(serializers.ModelSerializer):
    prices = RoomPriceSerializer(many=True, read_only=True)

    class Meta:
        model = HotelRoom
        fields = ['name', 'room_description', 'hotel', 'room_count', 'prices']
        depth = 1  # Adjust depth as needed


class CustomizedHotelSerializer(serializers.ModelSerializer):
    activities = serializers.ListField(child=serializers.DictField(), required=False)
    amenities = serializers.ListField(child=serializers.DictField(), required=False)
    hotel_info = serializers.DictField(required=False)
    hotel_rooms = serializers.ListField(child=serializers.DictField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    overall_rating = serializers.SerializerMethodField()
    instagram_link = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)
    booking_com_url = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)
    tripadvisor_url = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)
    website = serializers.CharField(validators=[flexible_url_validator], required=False, allow_blank=True)
    payment_types = PaymentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = CustomizedHotel
        fields = ['name', 'is_active', 'description', 'platform_hotel', 'region', 'google_place_id', 
                  'min_price_in_INR', 'hotel_owner', 'instagram_link', 'pet_friendly', 'payment_types', 
                  'activities', 'amenities', 'hotel_info', 'hotel_rooms', 'overall_rating', 
                  'booking_com_url', 'tripadvisor_url', 'tags', 'type', 'phone_number', 
                  'whatsapp_number', 'email', 'website']
        read_only_fields = ['overall_rating']

    def get_overall_rating(self, obj):
        if isinstance(obj, dict):
            return None
        if hasattr(obj, 'overall_rating'):
            return obj.overall_rating
        return None

    def to_representation(self, instance):
        try:
            data = super().to_representation(instance)
            request = self.context.get('request')

            if isinstance(instance, CustomizedHotel):
                if not (request and (request.user.is_superuser or request.user == instance.hotel_owner)):
                    data.pop('private_info', None)
                
                if hasattr(instance, 'hotel_owner') and instance.hotel_owner:
                    if not instance.hotel_owner.public_profile:
                        data.pop('hotel_owner', None)

            return data
        except Exception as e:
            print(f"Error in to_representation: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}  # Return an empty dict if there's an error

    def create(self, validated_data):
        try:
            activities_data = validated_data.pop('activities', [])
            amenities_data = validated_data.pop('amenities', [])
            hotel_info_data = validated_data.pop('hotel_info', None)
            hotel_rooms_data = validated_data.pop('hotel_rooms', [])
            tags_data = validated_data.pop('tags', [])
            payment_types_data = validated_data.pop('payment_types', [])

            print(f"Validated data: {validated_data}")  # Debug print

            # Prepend 'https://' to URL fields if not already present
            for field in ['instagram_link', 'booking_com_url', 'tripadvisor_url', 'website']:
                if validated_data.get(field) and not validated_data[field].startswith(('http://', 'https://')):
                    validated_data[field] = 'https://' + validated_data[field]

            hotel = CustomizedHotel.objects.create(**validated_data)
            print(f"Hotel created: {hotel}")  # Debug print

            self.create_activities(hotel, activities_data)
            self.create_amenities(hotel, amenities_data)
            if hotel_info_data:
                self.create_hotel_info(hotel, hotel_info_data)
            self.create_hotel_rooms(hotel, hotel_rooms_data)
            self.create_tags(hotel, tags_data)

            print(f"Related objects created")  # Debug print

            # Handle payment types
            print(f"Payment types data: {payment_types_data}")  # Debug print
            for payment_type_id in payment_types_data:
                payment_type = PaymentType.objects.get(id=payment_type_id)
                hotel.payment_types.add(payment_type)
            print(f"Payment types added")  # Debug print

            return hotel
        except Exception as e:
            print(f"Error in create method: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=False)
        if not valid:
            print(f"Validation errors: {self.errors}")
        return valid

    def update(self, instance, validated_data):
        activities_data = validated_data.pop('activities', [])
        amenities_data = validated_data.pop('amenities', [])
        hotel_info_data = validated_data.pop('hotel_info', None)
        hotel_rooms_data = validated_data.pop('hotel_rooms', [])
        tags_data = validated_data.pop('tags', [])
        payment_types_data = validated_data.pop('payment_types', [])

        # Prepend 'https://' to URL fields if not already present
        for field in ['instagram_link', 'booking_com_url', 'tripadvisor_url', 'website']:
            if validated_data.get(field) and not validated_data[field].startswith(('http://', 'https://')):
                validated_data[field] = 'https://' + validated_data[field]


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.hotel_activities.all().delete()
        self.create_activities(instance, activities_data)

        instance.hotel_amenities.all().delete()
        self.create_amenities(instance, amenities_data)

        if hotel_info_data:
            if hasattr(instance, 'hotel_info'):
                instance.hotel_info.delete()
            self.create_hotel_info(instance, hotel_info_data)

        instance.hotel_rooms.all().delete()
        self.create_hotel_rooms(instance, hotel_rooms_data)

        instance.tags.clear()
        self.create_tags(instance, tags_data)

        # Update payment types
        instance.payment_types.clear()
        for payment_type_id in payment_types_data:
            payment_type = PaymentType.objects.get(id=payment_type_id)
            instance.payment_types.add(payment_type)

        return instance


    def create_activities(self, hotel, activities_data):
        for activity_data in activities_data:
            HotelActivities.objects.create(customized_hotel=hotel, **activity_data)

    def create_amenities(self, hotel, amenities_data):
        for amenity_data in amenities_data:
            hotel_room_data = amenity_data.pop('hotel_room', None)
            if hotel_room_data:
                hotel_room, _ = HotelRoom.objects.get_or_create(customized_hotel=hotel, **hotel_room_data)
                HotelAmenities.objects.create(customized_hotel=hotel, hotel_room=hotel_room, **amenity_data)
            else:
                HotelAmenities.objects.create(customized_hotel=hotel, **amenity_data)

    def create_hotel_info(self, hotel, hotel_info_data):
        HotelInfo.objects.create(customized_hotel=hotel, **hotel_info_data)

    def create_hotel_rooms(self, hotel, hotel_rooms_data):
        for room_data in hotel_rooms_data:
            HotelRoom.objects.create(customized_hotel=hotel, **room_data)

    def create_tags(self, hotel, tags_data):
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            hotel.tags.add(tag)

    def update_activities(self, hotel, activities_data):
        hotel.hotel_activities.all().delete()
        self.create_activities(hotel, activities_data)

    def update_amenities(self, hotel, amenities_data):
        hotel.hotel_amenities.all().delete()
        self.create_amenities(hotel, amenities_data)

    def update_hotel_info(self, hotel, hotel_info_data):
        if hasattr(hotel, 'hotel_info'):
            hotel.hotel_info.delete()
        self.create_hotel_info(hotel, hotel_info_data)

    def update_hotel_rooms(self, hotel, hotel_rooms_data):
        hotel.hotel_rooms.all().delete()
        self.create_hotel_rooms(hotel, hotel_rooms_data)

    def update_tags(self, hotel, tags_data):
        hotel.tags.clear()
        self.create_tags(hotel, tags_data)

class AgentHotelSerializer(serializers.ModelSerializer):
    agent_hotel_rooms = HotelRoomSerializer(many=True, source='agent_hotel_rooms')

    class Meta:
        model = AgentHotel
        fields = '__all__'
        read_only_fields = ['parent_hotel']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if not (request and (request.user.is_superuser or request.user == instance.agent)):
            data.pop('tac_percentage', None)
        return data
