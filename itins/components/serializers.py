from .models import ComponentType, Component
from rest_framework import serializers
from hotels.serializers import HotelRoomSerializer
from contacts.serializers import ContactSerializer
from contacts.models import Contact
from hotels.models import HotelRoom

class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ['id', 'name', 'agent', 'is_deletable']

# Checks if ComponentType belongs to a logged in agent and is not a global type (HotelRoom etc) before allowing updates

    def update(self, instance, validated_data):
        # Get the agent from the context (assuming it's passed in the request context)
        agent = self.context['request'].user.agent

        # Check if the instance belongs to the agent and is not a global type
        if instance.agent == agent and not instance.is_global_type:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("You do not have permission to edit this component type.")

    def delete(self, instance):
        # Get the agent from the context
        agent = self.context['request'].user.agent

        # Check if the instance can be deleted and belongs to the agent
        if instance.agent == agent and instance.is_deletable and not instance.is_global_type:
            instance.delete()
        else:
            raise serializers.ValidationError("You do not have permission to delete this component type.")

class ComponentSerializer(serializers.ModelSerializer):
    hotel_room = HotelRoomSerializer(read_only=False, required=False, allow_null=True)
    contact = ContactSerializer(read_only=False)

    class Meta:
        model = Component
        fields = [
            'agent', 'name', 'hotel_room', 'description', 'contact', 
            'price_for_1_pax', 'price_for_2_pax', 'price_for_3_pax', 'price_for_4_pax', 
            'fixed_price_overall', 'fixed_price_per_person', 'net_price_for_1_pax', 
            'net_price_for_2_pax', 'net_price_for_3_pax', 'net_price_for_4_pax', 
            'net_fixed_price_overall', 'net_fixed_price_per_person'
        ]


    def create(self, validated_data):
        hotel_room_data = validated_data.pop('hotel_room', None)
        contact_data = validated_data.pop('contact', None)

        # Create the Contact instance
        contact = Contact.objects.create(**contact_data)
        validated_data['contact'] = contact

        # Create or update the HotelRoom instance
        hotel_room = None
        if hotel_room_data:
            hotel_room = HotelRoom.objects.create(**hotel_room_data)
            validated_data['hotel_room'] = hotel_room

        component = Component.objects.create(**validated_data)
        return component

    def update(self, instance, validated_data):
        hotel_room_data = validated_data.pop('hotel_room', None)
        contact_data = validated_data.pop('contact', None)

        # Update the Contact instance
        for attr, value in contact_data.items():
            setattr(instance.contact, attr, value)
        instance.contact.save()

        # Update the HotelRoom instance if provided
        if hotel_room_data:
            if instance.hotel_room:
                for attr, value in hotel_room_data.items():
                    setattr(instance.hotel_room, attr, value)
                instance.hotel_room.save()
            else:
                instance.hotel_room = HotelRoom.objects.create(**hotel_room_data)

        # Update the Component instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
# Checks if Component belongs to a logged in agent before returning
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Filter Components by ComponentType and Agent ID
        if instance.agent_id != self.context['request'].user.agent.id:
            return {}  # Or handle as needed
        return representation
