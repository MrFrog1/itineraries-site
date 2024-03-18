from rest_framework import serializers
from region.serializers import RegionSerializer
from contacts.serializers import ContactSerializer
from .models import Itinerary, ItineraryGroup, ItineraryGrouping, ItineraryDay, ItineraryDayComponent, CustomerItinerary, AgentItinerary


class ItineraryDayComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryDayComponent
        fields = ['id', 'itinerary_day', 'component', 'customer', 'customer_note', 'price', 'net_price', 'customer_price_markup_percentage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user

        # Hide net price for customers
        if hasattr(user, 'customer'):
            representation.pop('net_price', None)

        if not instance.price_visible:
            representation.pop('price', None)

        return representation
    



class ItineraryDaySerializer(serializers.ModelSerializer):
    itinerary_day_components = ItineraryDayComponentSerializer(many=True, read_only=True)

    class Meta:
        model = ItineraryDay
        fields = ['id', 'name', 'itinerary_day_components']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add logic here to calculate and add totals to the representation if needed
        # totals = instance.calculate_totals()
        # representation['totals'] = totals

        if not instance.price_visible:
            representation.pop('price', None)
            
        return representation


class ItineraryGroupSerializer(serializers.ModelSerializer):
    guide = ContactSerializer(read_only=True)
    itinerary_days = ItineraryDaySerializer(many=True, read_only=True)  # Assuming you have an ItineraryDay model related to ItineraryGroup

    class Meta:
        model = ItineraryGroup
        fields = [
            'id', 'name', 'mandatory_guide', 'mandatory_position_in_itinerary', 'guide', 
            'override_cost_for_1_pax', 'override_cost_for_2_pax', 'override_cost_for_3_pax', 
            'override_cost_for_4_pax', 'description', 'itinerary_days'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Here you can add any additional logic needed for representing an ItineraryGroup.
        # For example, you might want to add calculated total costs or other derived data.

        return representation


class ItineraryGroupingSerializer(serializers.ModelSerializer):
    itinerary_days = ItineraryDaySerializer(many=True, read_only=True)

    class Meta:
        model = ItineraryGrouping
        fields = ['id', 'customer_itinerary', 'agent_itinerary', 'group', 'itinerary_days']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add any additional logic here if needed
        return representation
    

class ItinerarySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    guide = ContactSerializer(read_only=True)
    itinerary_groups = ItineraryGroupingSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)  # Assuming your model has this field

    class Meta:
        model = Itinerary
        fields = ['name', 'description', 'internal_notes_for_agent', 'customisable', 'category',
                  'region', 'cost_for_1_pax', 'cost_for_2_pax', 'cost_for_3_pax', 'cost_for_4_pax',
                  'cost_with_tour_leader_1_pax', 'agent', 'expert', 'guide', 'agent_made', 
                  'verified_by_admin', 'customised_by_guest', 'itinerary_parent', 'price_breakdown', 
                  'january_rating', 'february_rating', 'march_rating', 'april_rating', 'may_rating', 
                  'june_rating', 'july_rating', 'august_rating', 'september_rating', 'october_rating', 
                  'november_rating', 'december_rating', 'customer', 'itinerary_groups', 'total_price', 
                  'created_at']

    def get_total_price(self, obj):
        # Implement the logic to calculate the total price based on ItineraryGroups
        total_price = 0
        for group in obj.itinerary_groups.all():
            # Calculate the price per group and add to total_price
            pass
        return total_price

    def validate_name(self, value):
        # Custom validation for the name field
        if Itinerary.objects.filter(name=value).exists():
            raise serializers.ValidationError("An itinerary with this name already exists.")
        return value


    def to_representation(self, instance):
        # Delayed import
        from customers.serializers import UserSerializer
        ret = super().to_representation(instance)
        ret['agent'] = UserSerializer(instance.agent, read_only=True).data
        ret['customer'] = UserSerializer(instance.customer, read_only=True).data
        return ret
    
    # Add other validation methods as 
    
class CustomerItinerarySerializer(serializers.ModelSerializer):
    agent_itinerary = serializers.PrimaryKeyRelatedField(read_only=True)
    itinerary_days = ItineraryDaySerializer(many=True, read_only=True)

    class Meta:
        model = CustomerItinerary
        fields = ['id', 'agent_itinerary', 'customer', 'customer_notes', 'number_of_adults', 'number_of_children_6_to_12', 'number_of_infants_0_to_5', 'number_of_taxis', 'number_of_rooms', 'agent_listed_cost', 'confirmed', 'itinerary_days']
        read_only_fields = ['agent_listed_cost', 'confirmed']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Hide sensitive pricing details based on certain conditions
        if instance.override_price:
            representation.pop('agent_listed_cost', None)

        # Ensure net prices and price breakdowns are not visible to customers
        for day in representation.get('itinerary_days', []):
            for component in day.get('itinerary_day_components', []):
                component.pop('net_price', None)

        from customers.serializers import UserSerializer       
        representation['customer'] = UserSerializer(instance.customer, read_only=True).data
        return representation


class AgentItinerarySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    guide = ContactSerializer(read_only=True)
    itinerary_groups = ItineraryGroupingSerializer(many=True, read_only=True)

    class Meta:
        model = AgentItinerary
        fields = ['id', 'name', 'region', 'agent', 'expert', 'guide', 'category', 'customisable', 'cost_for_1_pax', 'cost_for_2_pax', 'cost_for_3_pax', 'cost_for_4_pax', 'with_leader_cost_for_1_pax', 'with_leader_cost_for_2_pax', 'with_leader_cost_for_3_pax', 'with_leader_cost_for_4_pax', 'visible_description', 'price_breakdown', 'itinerary_groups']
        read_only_fields = ['price_breakdown']  # Assuming price_breakdown should not be editable

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Hide the price breakdown if it should not be visible
        if not instance.price_breakdown_visible:
            representation.pop('price_breakdown', None)

        from customers.serializers import UserSerializer       
        representation['agent'] = UserSerializer(instance.agent, read_only=True).data
        representation['expert'] = UserSerializer(instance.expert, read_only=True).data

        return representation
    

        return representation
