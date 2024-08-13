from .models import ComponentType, Component
from rest_framework import serializers
from hotels.serializers import HotelRoomSerializer
from contacts.serializers import ContactSerializer
from contacts.models import Contact
from hotels.models import HotelRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ComponentTypeSerializer(serializers.ModelSerializer):
    agent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ComponentType
        fields = ['id', 'name', 'agent', 'is_deletable','is_global']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['agent'] = {
            'id': instance.agent.id,
            'username': instance.agent.username,
            'first_name': instance.agent.first_name,
            'last_name': instance.agent.last_name
        }
        return representation
    
# Checks if ComponentType belongs to a logged in agent and is not a global type (HotelRoom etc) before allowing updates
    def create(self, validated_data):
        agent = validated_data.pop('agent', None)
        if agent is None:
            agent = self.context['request'].user
        return ComponentType.objects.create(agent=agent, **validated_data)

    def update(self, instance, validated_data):
        # Get the agent from the context (assuming it's passed in the request context)
        agent = self.context['request'].user.agent

        # Check if the instance belongs to the agent and is not a global type
        if instance.agent == agent and not instance.is_global:
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
    hotel_room = HotelRoomSerializer(read_only=True, required=False)
    contact = ContactSerializer(required=False, allow_null=True)
    component_type = ComponentTypeSerializer(read_only=True)
    component_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ComponentType.objects.all(), source='component_type', write_only=True
    )


    class Meta:
        model = Component
        fields = [
            'id', 'agent', 'name', 'description', 'component_type', 'component_type_id',
            'hotel_room', 'is_platform_experience', 'is_visible_to_all',
            'wheelchair_accessible', 'age_limit', 'fitness_level', 'contact',
            'price_for_1_pax', 'price_for_2_pax', 'price_for_3_pax', 'price_for_4_pax',
            'fixed_price_overall', 'fixed_price_per_person',
            'net_price_for_1_pax', 'net_price_for_2_pax', 'net_price_for_3_pax', 'net_price_for_4_pax',
            'net_fixed_price_overall', 'net_fixed_price_per_person'
        ]

    def create(self, validated_data):
        hotel_room_data = validated_data.pop('hotel_room', None)
        contact_data = validated_data.pop('contact', None)

        # Create the Contact instance
        if contact_data:
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

        # Update the Contact instance if provided
        if contact_data:
            if instance.contact:
                for attr, value in contact_data.items():
                    setattr(instance.contact, attr, value)
                instance.contact.save()
            else:
                contact = Contact.objects.create(**contact_data)
                instance.contact = contact

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
        request = self.context.get('request')
        
        if request and request.user:
            # Check if the user is an admin or superuser
            if request.user.is_superuser or request.user.is_staff:
                return representation  # Return full representation for admins
            
            # For non-admin users, check if the component belongs to them
            if instance.agent_id == request.user.id:
                return representation
            
            # If it's not the user's component and they're not an admin, return an empty dict or handle as needed
            return {}
        
        # If there's no authenticated user (e.g., public API), decide what to return
        return representation if instance.is_public else {}  # Assuming you have an is_public field, adjust as needed


# Claude recommended this functionality
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     user = self.context['request'].user
        
    #     if not user.is_staff:
    #         if not instance.is_visible_to_all and instance.agent != user:
    #             return None
            
    #         if instance.hotel_room and not instance.hotel_room.customized_hotel.is_visible_to_all:
    #             return None

    #         # Remove net price fields for non-staff users
    #         for field in ['net_price_for_1_pax', 'net_price_for_2_pax', 'net_price_for_3_pax', 'net_price_for_4_pax',
    #                       'net_fixed_price_overall', 'net_fixed_price_per_person']:
    #             representation.pop(field, None)

    #     return representation

    # def transfer_to_agent(self, instance, new_agent):
    #     return instance.transfer_to_agent(new_agent)

    # @classmethod
    # def create_for_agents(cls, agents, validated_data):
    #     return Component.create_for_agents(agents, **validated_data)