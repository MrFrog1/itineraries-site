from rest_framework import serializers
from .models import Hotel, CustomizedHotel, AgentHotel, HotelRoom, RoomPrice, HotelActivities, HotelAmenities, HotelInfo
from common.serializers import  TagSerializer
from reviews.serializers import ExternalReviewSerializer

# These use CustomizedHotel as a default - as these are the ones on the platform. Once the apop matures into adding random hotels that
# dont have information, then we can add different ones that use just the Hotel model


class BasicHotelSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    overall_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = CustomizedHotel
        fields = ['id', 'name', 'description', 'region', 'type', 'tags', 'min_price_in_INR', 'is_active','overall_rating']

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
    activities = HotelActivitiesSerializer(many=True, source='hotel_activities', required=False)
    amenities = HotelAmenitiesSerializer(many=True, source='hotel_amenities', required=False)
    hotel_info = HotelInfoSerializer(source='hotel_info.first', required=False)
    hotel_rooms = HotelRoomSerializer(many=True, source='hotel_rooms', required=False)

    class Meta:
        model = CustomizedHotel
        fields = ['name', 'is_active', 'description', 'platform_hotel', 'region', 'google_place_id', 'longitude', 'latitude', 'min_price_in_INR', 'hotel_owner', 'instagram_link', 'pet_friendly', 'payment_types', 'activities', 'amenities', 'hotel_info', 'rating', 'booking_com_url', 'tripadvisor_url']
        read_only_fields = ['rating', 'hotel_owner']

    def create(self, validated_data):
        activities_data = validated_data.pop('hotel_activities', [])
        amenities_data = validated_data.pop('hotel_amenities', [])
        hotel_info_data = validated_data.pop('hotel_info', None)
        hotel_rooms_data = validated_data.pop('hotel_rooms', [])

        hotel = CustomizedHotel.objects.create(**validated_data)

        self.create_activities(hotel, activities_data)
        self.create_amenities(hotel, amenities_data)
        if hotel_info_data:
            self.create_hotel_info(hotel, hotel_info_data)
        self.create_hotel_rooms(hotel, hotel_rooms_data)

        return hotel


    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)

        # Exclude private information for non-hotel owners or non-admins
        if not (request and (request.user.is_superuser or request.user == instance.hotel_owner.user)):
            data.pop('private_info', None)

        # Exclude hotel_owner information if their profile is not public
        if instance.hotel_owner and not instance.hotel_owner.public_profile:
            data.pop('hotel_owner', None)

        return data
    
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)

        # Exclude private information for non-hotel owners or non-admins
        if not (request and (request.user.is_superuser or request.user == instance.hotel_owner)):
            data.pop('private_info', None)

        # Exclude hotel_owner information if their profile is not public
        if instance.hotel_owner and not instance.hotel_owner.public_profile:
            data.pop('hotel_owner', None)

        return data
    


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
