# populate_itineraries.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from components.models import ComponentType, Component
from contacts.models import Contact
from hotels.models import HotelRoom
from itineraries.models import (
    AgentItinerary, CustomerItinerary, ItineraryGroup, ItineraryGrouping,
    ItineraryDay, ItineraryDayComponent, RoomSpecification
)
from region.models import Region
from common.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with itinerary data and related models'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting itinerary data population...'))

        with transaction.atomic():
            self.create_component_types()
            self.create_components()
            self.create_agent_itineraries()
            self.create_customer_itineraries()
            self.create_itinerary_groups()
            self.create_itinerary_groupings()
            self.create_itinerary_days()
            self.create_itinerary_day_components()
            self.create_room_specifications()

        self.stdout.write(self.style.SUCCESS('Finished populating itinerary data'))

    def create_component_types(self):
        component_types_data = [
            {"name": "Hotel", "is_deletable": False},
            {"name": "Transportation", "is_deletable": True},
            {"name": "Activity", "is_deletable": True},
            # Add more component types as needed
        ]

        for type_data in component_types_data:
            ComponentType.objects.get_or_create(name=type_data['name'], defaults=type_data)

        self.stdout.write(self.style.SUCCESS('Created component types'))

    def create_components(self):
        components_data = [
            {
                "name": "Luxury Hotel Stay",
                "description": "A night in a luxurious hotel",
                "agent": User.objects.get(username="example_agent"),
                "contact": Contact.objects.get(name="Hotel Contact"),
                "price_for_1_pax": 200,
                "price_for_2_pax": 250,
                "fitness_level": "easy",
            },
            # Add more component data as needed
        ]

        for comp_data in components_data:
            Component.objects.get_or_create(name=comp_data['name'], agent=comp_data['agent'], defaults=comp_data)

        self.stdout.write(self.style.SUCCESS('Created components'))

    def create_agent_itineraries(self):
        itineraries_data = [
            {
                "name": "Luxury Getaway",
                "region": Region.objects.get(name="Example Region"),
                "agent": User.objects.get(username="example_agent"),
                "type": "cultural",
                "cost_for_1_pax": 1000,
                "cost_for_2_pax": 1500,
                "short_visible_description": "A luxurious cultural experience",
            },
            # Add more itinerary data as needed
        ]

        for itin_data in itineraries_data:
            AgentItinerary.objects.get_or_create(name=itin_data['name'], agent=itin_data['agent'], defaults=itin_data)

        self.stdout.write(self.style.SUCCESS('Created agent itineraries'))

    def create_customer_itineraries(self):
        customer_itineraries_data = [
            {
                "original_itinerary": AgentItinerary.objects.get(name="Luxury Getaway"),
                "customer": User.objects.get(username="example_customer"),
                "number_of_adults": 2,
                "number_of_children_6_to_12": 1,
                "number_of_infants_0_to_5": 0,
                "number_of_taxis": 1,
                "number_of_rooms": 1,
            },
            # Add more customer itinerary data as needed
        ]

        for cust_itin_data in customer_itineraries_data:
            CustomerItinerary.objects.get_or_create(
                original_itinerary=cust_itin_data['original_itinerary'],
                customer=cust_itin_data['customer'],
                defaults=cust_itin_data
            )

        self.stdout.write(self.style.SUCCESS('Created customer itineraries'))

    def create_itinerary_groups(self):
        groups_data = [
            {
                "name": "City Tour",
                "description": "Explore the city's main attractions",
                "mandatory_guide": True,
            },
            # Add more group data as needed
        ]

        for group_data in groups_data:
            ItineraryGroup.objects.get_or_create(name=group_data['name'], defaults=group_data)

        self.stdout.write(self.style.SUCCESS('Created itinerary groups'))

    def create_itinerary_groupings(self):
        groupings_data = [
            {
                "customer_itinerary": CustomerItinerary.objects.first(),
                "agent_itinerary": AgentItinerary.objects.first(),
                "group": ItineraryGroup.objects.get(name="City Tour"),
                "visible_guide": True,
            },
            # Add more grouping data as needed
        ]

        for grouping_data in groupings_data:
            ItineraryGrouping.objects.get_or_create(
                customer_itinerary=grouping_data['customer_itinerary'],
                agent_itinerary=grouping_data['agent_itinerary'],
                group=grouping_data['group'],
                defaults=grouping_data
            )

        self.stdout.write(self.style.SUCCESS('Created itinerary groupings'))

    def create_itinerary_days(self):
        days_data = [
            {
                "name": "Day 1: City Exploration",
                "description": "Explore the city's landmarks",
                "itinerary_group": ItineraryGroup.objects.get(name="City Tour"),
            },
            # Add more day data as needed
        ]

        for day_data in days_data:
            ItineraryDay.objects.get_or_create(
                name=day_data['name'],
                itinerary_group=day_data['itinerary_group'],
                defaults=day_data
            )

        self.stdout.write(self.style.SUCCESS('Created itinerary days'))

    def create_itinerary_day_components(self):
        day_components_data = [
            {
                "itinerary_day": ItineraryDay.objects.get(name="Day 1: City Exploration"),
                "component": Component.objects.get(name="Luxury Hotel Stay"),
                "customer": User.objects.get(username="example_customer"),
                "customer_note": "Special requests: Late check-in",
            },
            # Add more day component data as needed
        ]

        for day_comp_data in day_components_data:
            ItineraryDayComponent.objects.get_or_create(
                itinerary_day=day_comp_data['itinerary_day'],
                component=day_comp_data['component'],
                customer=day_comp_data['customer'],
                defaults=day_comp_data
            )

        self.stdout.write(self.style.SUCCESS('Created itinerary day components'))

    def create_room_specifications(self):
        room_specs_data = [
            {
                "customer_itinerary": CustomerItinerary.objects.first(),
                "component": Component.objects.get(name="Luxury Hotel Stay"),
                "adults_in_room": 2,
                "children_in_room": 1,
            },
            # Add more room specification data as needed
        ]

        for room_spec_data in room_specs_data:
            RoomSpecification.objects.get_or_create(
                customer_itinerary=room_spec_data['customer_itinerary'],
                component=room_spec_data['component'],
                defaults=room_spec_data
            )

        self.stdout.write(self.style.SUCCESS('Created room specifications'))