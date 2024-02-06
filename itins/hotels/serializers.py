from rest_framework import serializers
from .models import Hotel, CustomizedHotel, AgentHotel, HotelRoom, RoomPrice, HotelActivities, HotelAmenities, HotelInfo


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
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

class HotelRoomSerializer(serializers.ModelSerializer):
    prices = RoomPriceSerializer(many=True, read_only=True)

    class Meta:
        model = HotelRoom
        fields = ['name', 'room_description', 'hotel', 'room_count', 'prices']
        depth = 1  # Adjust depth as needed

class CustomizedHotelSerializer(serializers.ModelSerializer):
    activities = HotelActivitiesSerializer(many=True, source='hotel_activities')  
    amenities = HotelAmenitiesSerializer(many=True, source='hotel_amenities')      
    hotel_info = HotelInfoSerializer(source='hotel_info.first')              
    hotel_rooms = HotelRoomSerializer(many=True, source='hotel_rooms') 



    class Meta:
        model = CustomizedHotel
        fields = ['name', 'is_active', 'description', 'platform_hotel', 'region', 'google_place_id', 'longitude', 'latitude', 'min_price_in_INR','hotel_owner', 'instagram_link', 'pet_friendly', 'payment_types', 'activities', 'amenities', 'hotel_info', 'rating']
        read_only_fields = ['rating']

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

class AgentHotelSerializer(serializers.ModelSerializer):
    agent_hotel_rooms = HotelRoomSerializer(many=True, source='agent_hotel_rooms')

    class Meta:
        model = AgentHotel
        fields = '__all__'
        read_only_fields = ['parent_hotel']

    