# populate_hotels.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from hotels.models import CustomizedHotel, HotelRoom
from region.models import Region, RegionSubsection
from common.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with hotel data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting hotel population...'))

        tags = self.create_tags()

        # Hotel data
        hotels_data = [
            {
                "name": "Example Hotel",
                "description": "An example hotel description.",
                "min_price_in_INR": 10000,
                "type": "Example Type",
                "google_place_id": "example_place_id",
                "region_name": "Ladakh",
                "region_subsection": "Example Subsection",
                "hotel_owner": "example_username",
                "pet_friendly": False,
                "wheelchair_accessible": True,
                "serves_alcohol": False,
                "tags": ["Example Tag 1", "Example Tag 2"],
                "rooms": [
                    {
                        "name": "Example Room",
                        "description": "An example room description.",
                        "size": 300,
                        "count": 5
                    },
                    # Add more room dictionaries here
                ]
            },
            # Add more hotel data dictionaries here
        ]

        self.create_hotels(hotels_data, tags)

        self.stdout.write(self.style.SUCCESS('Finished populating hotels'))

    def create_tags(self):
        tag_names = [
            "Example Tag 1", "Example Tag 2", "Example Tag 3",
            # Add more tag names here
        ]
        tags = {}
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags[name] = tag
        return tags

    def create_hotels(self, hotels_data, tags):
        for hotel_data in hotels_data:
            try:
                region = Region.objects.get(name=hotel_data["region_name"])
                region_subsection, _ = RegionSubsection.objects.get_or_create(
                    name=hotel_data["region_subsection"],
                    region=region
                )
                
                hotel_owner = User.objects.get(username=hotel_data["hotel_owner"])

                hotel, created = CustomizedHotel.objects.update_or_create(
                    name=hotel_data["name"],
                    defaults={
                        "description": hotel_data["description"],
                        "platform_hotel": True,
                        "min_price_in_INR": hotel_data["min_price_in_INR"],
                        "is_active": True,
                        "type": hotel_data["type"],
                        "google_place_id": hotel_data.get("google_place_id"),
                        "region": region,
                        "region_subsection": region_subsection,
                        "hotel_owner": hotel_owner,
                        "pet_friendly": hotel_data["pet_friendly"],
                        "wheelchair_accessible": hotel_data["wheelchair_accessible"],
                        "serves_alcohol": hotel_data["serves_alcohol"],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated hotel: {hotel.name}'))

                hotel.tags.clear()
                for tag_name in hotel_data["tags"]:
                    hotel.tags.add(tags[tag_name])

                for room_data in hotel_data.get("rooms", []):
                    HotelRoom.objects.update_or_create(
                        name=room_data["name"],
                        customized_hotel=hotel,
                        defaults={
                            "room_description": room_data["description"],
                            "room_size_sq_ft": room_data["size"],
                            "room_count": room_data["count"],
                        }
                    )

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {hotel_data["hotel_owner"]} does not exist'))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f'Validation error creating/updating hotel {hotel_data["name"]}: {str(e)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating/updating hotel {hotel_data["name"]}: {str(e)}'))