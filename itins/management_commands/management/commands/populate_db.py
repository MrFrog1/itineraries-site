# management/commands/populate_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from customers.models import AgentProfile
from hotels.models import CustomizedHotel
from itineraries.models import AgentItinerary
from region.models import Region
from common.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create or get regions
        regions = []
        for region_data in [
            {"name": "Rajasthan", "description": "Land of Kings"},
            {"name": "Kerala", "description": "God's Own Country"},
            {"name": "Goa", "description": "Pearl of the Orient"},
        ]:
            existing_regions = Region.objects.filter(name=region_data["name"])
            if existing_regions.exists():
                regions.append(existing_regions.first())
                self.stdout.write(f"Using existing region: {region_data['name']}")
            else:
                new_region = Region.objects.create(**region_data)
                regions.append(new_region)
                self.stdout.write(f"Created new region: {region_data['name']}")

        # Create tags
        tags = [
            Tag.objects.get_or_create(name="Luxury")[0],
            Tag.objects.get_or_create(name="Budget")[0],
            Tag.objects.get_or_create(name="Adventure")[0],
            Tag.objects.get_or_create(name="Relaxation")[0]
        ]

        # Create agents
        agents = []
        for i in range(3):
            username = f"agent{i}"
            email = f"agent{i}@example.com"
            
            try:
                user = User.objects.create_user(username, email, "password")
                user.is_agent = True
                user.save()
                AgentProfile.objects.get_or_create(user=user, defaults={"bio": f"Agent {i} bio"})
                agents.append(user)
            except IntegrityError:
                self.stdout.write(f"User {username} already exists. Skipping...")
                existing_user = User.objects.get(username=username)
                if existing_user.is_agent:
                    agents.append(existing_user)
                else:
                    self.stdout.write(f"User {username} exists but is not an agent. Skipping...")

        if not agents:
            self.stdout.write("No agents created or found. Exiting.")
            return

        # Create hotels
        for i in range(10):
            hotel, created = CustomizedHotel.objects.get_or_create(
                name=f"Hotel {i}",
                defaults={
                    "description": f"Description for Hotel {i}",
                    "region": regions[i % len(regions)],
                    "rating": i % 5 + 1,
                    "type": "luxury" if i % 2 == 0 else "budget",
                    "min_price_in_INR": (i + 1) * 1000,
                    "is_active": True,
                    "hotel_owner": agents[i % len(agents)],
                    "platform_hotel": True,
                    "instagram_link": f"https://instagram.com/hotel{i}",
                    "pet_friendly": i % 2 == 0,
                    "wheelchair_accessible": i % 3 == 0,
                    "serves_alcohol": i % 2 != 0,
                }
            )
            if created:
                hotel.tags.add(tags[i % 4])

        # Create itineraries
        for i in range(10):
            itinerary, created = AgentItinerary.objects.get_or_create(
                name=f"Itinerary {i}",
                defaults={
                    "region": regions[i % len(regions)],
                    "agent": agents[i % len(agents)],
                    "cost_for_1_pax": (i + 1) * 5000,
                    "cost_for_2_pax": (i + 1) * 8000,
                    "cost_for_3_pax": (i + 1) * 11000,
                    "cost_for_4_pax": (i + 1) * 14000,
                    "short_visible_description": f"Short description for Itinerary {i}",
                    "visible_description": f"Visible description for Itinerary {i}",
                    "type": "hiking" if i % 2 == 0 else "cultural",
                    "customisable": i % 2 == 0,
                }
            )
            if created:
                itinerary.tags.add(tags[i % 4])

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))