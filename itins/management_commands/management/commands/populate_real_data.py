from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from hotels.models import CustomizedHotel, HotelRoom
from customers.models import AgentProfile
from region.models import Region, RegionSubsection
from common.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Add missing hotels: Shan at Uley and Drenmo Lodge'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to add missing hotels...'))

        tags = {tag.name: tag for tag in Tag.objects.all()}

        hotels_data = [
            {
                "name": "Shan at Uley",
                "description": "A cosy winter lodge high in the mountains, in the land of the Shan (snow leopard)",
                "min_price_in_INR": 20000,
                "type": "Wildlife and Jungle Lodges",
                "google_place_id": "ChIJfQygJk4J_TgRdcowW2V_sNA",
                "region_name": "Ladakh",
                "region_subsection": "Sham Valley",
                "hotel_owner": "morup_namgial",
                "pet_friendly": False,
                "wheelchair_accessible": False,
                "serves_alcohol": False,
                "tags": ["Natural Space", "Environmentally Conscious", "Wild and Remote", "Experiential", "Staying with a Family"],
                "rooms": []
            },
            {
                "name": "Drenmo Lodge",
                "description": "Tucked away in the Mushkow Valley, set in an extraordinary vantage point, Drenmo is the ultimate lodge for spotting the Himalayan Brown Bear - most viewings are visible from its own veranda",
                "min_price_in_INR": 25000,
                "type": "Wildlife and Jungle Lodges",
                "google_place_id": "ChIJfVYnPYqr4zgRqKQPe8zsb1o",
                "region_name": "Ladakh",
                "region_subsection": "Mushkow Valley",
                "hotel_owner": "muzammil_hussain",
                "pet_friendly": False,
                "wheelchair_accessible": False,
                "serves_alcohol": False,
                "tags": ["Natural Space", "Environmentally Conscious", "Wild and Remote", "Experiential"],
                "rooms": []
            }
        ]

        for hotel_data in hotels_data:
            try:
                region = Region.objects.get(name=hotel_data["region_name"])
                region_subsection = RegionSubsection.objects.get(name=hotel_data["region_subsection"], region=region)
                
                # Get the User instance directly
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
                        "hotel_owner": hotel_owner,  # This is now a User instance
                        "pet_friendly": hotel_data["pet_friendly"],
                        "wheelchair_accessible": hotel_data["wheelchair_accessible"],
                        "serves_alcohol": hotel_data["serves_alcohol"],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated hotel: {hotel.name}'))

                # Clear existing tags and add new ones
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

        self.stdout.write(self.style.SUCCESS('Finished adding/updating missing hotels'))



# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from datetime import timedelta
# from django.db import IntegrityError, transaction
# from django.core.exceptions import ValidationError
# from hotels.models import CustomizedHotel, HotelRoom
# from customers.models import AgentProfile, ExpertiseCategory
# from region.models import Region, RegionSubsection
# from common.models import Tag
# from reviews.models import ExternalReviewSource

# User = get_user_model()

# class Command(BaseCommand):
#     help = 'Populate database with real hotel and itinerary data'

#     def handle(self, *args, **kwargs):
#         self.stdout.write(self.style.SUCCESS('Starting database population...'))

#         # Create ExpertiseCategories
#         self.create_expertise_categories()

#         # Create Region and RegionSubsections
#         ladakh = self.create_regions_and_subsections()

#         # Create Agents
#         self.create_agents(ladakh)

#         # Create ExternalReviewSources
#         self.create_external_review_sources()

#         # Create Tags
#         tags = self.create_tags()

#         # Create Hotels
#         self.create_hotels(tags)

#         # Diagnose AgentProfiles
#         self.diagnose_agent_profiles()

#         self.stdout.write(self.style.SUCCESS('Successfully populated database with real data'))

#     def create_expertise_categories(self):
#         categories = ["Snow Leopard Tours", "Cultural Tours", "Motorbike Tours", "Wildlife Tours"]
#         for category in categories:
#             ExpertiseCategory.objects.get_or_create(name=category)
#         self.stdout.write(self.style.SUCCESS('Created expertise categories'))

#     def create_regions_and_subsections(self):
#         ladakh, _ = Region.objects.get_or_create(name="Ladakh")
#         subsections = [
#             'Nubra Valley', 'Sham Valley', 'Leh', 'Indus Valley', 
#             'Pangong Lake', 'Tso Moriri Lake', 'Changtang', 'Hanle', 
#             'Zanskar Valley', 'Markha Valley', 'Kargil', 'Mushkow Valley'
#         ]
#         for subsection in subsections:
#             RegionSubsection.objects.get_or_create(name=subsection, region=ladakh)
#         self.stdout.write(self.style.SUCCESS('Created region and subsections'))
#         return ladakh


#     def create_agents(self, ladakh):
#         self.stdout.write(self.style.NOTICE("Starting agent creation process..."))
#         today = timezone.now().date()
#         agents_data = [
#             {
#                 'username': 'gulzar_hussain',
#                 'first_name': 'Gulzar',
#                 'last_name': 'Hussain',
#                 'email': 'gulzar.stalam@gmail.com',
#                 'phone_number': '+91 88034 25501',
#                 'business_name': 'Frozen Himalayas',
#                 'instagram_link': 'https://www.instagram.com/gulzar.himalayas/',
#                 'expertise_categories': ['Snow Leopard Tours', 'Cultural Tours'],
#                 'agent_starting_date': today - timedelta(days=12*365),
#             },
#             {
#                 'username': 'vikram_nimmu',
#                 'first_name': 'Vikram',
#                 'last_name': '',
#                 'email': 'contact@nimmu-house.com',
#                 'phone_number': '+91 99998 45726',
#                 'business_name': 'Nimmu House',
#                 'hotel_owner': True,
#                 'agent_starting_date': today - timedelta(days=15*365),
#             },
#             {
#                 'username': 'morup_namgial',
#                 'first_name': 'Morup',
#                 'last_name': 'Namgial',
#                 'email': 'shanatuley@gmail.com',
#                 'phone_number': '+91 97973 44047',
#                 'business_name': 'Shan at Uley',
#                 'instagram_link': 'https://www.instagram.com/morup_namgail',
#                 'hotel_owner': True,
#                 'expertise_categories': ['Snow Leopard Tours'],
#                 'agent_starting_date': today - timedelta(days=7*365),
#             },
#             {
#                 'username': 'rinchen_kalon',
#                 'first_name': 'Rinchen',
#                 'last_name': 'Kalon',
#                 'email': 'thekyagar@gmail.com',
#                 'phone_number': '+91 98104 27145',
#                 'business_name': 'The Kyagar',
#                 'hotel_owner': True,
#                 'agent_starting_date': today - timedelta(days=15*365),
#             },
#             {
#                 'username': 'nico_toller',
#                 'first_name': 'Nico',
#                 'last_name': 'Toller',
#                 'email': 'theindusrivercamp@gmail.com',
#                 'phone_number': '+91 7051379442',
#                 'business_name': 'The Indus River Cam',
#                 'hotel_owner': True,
#                 'agent_starting_date': today - timedelta(days=8*365),
#             },
#             {
#                 'username': 'hashim_qayoom',
#                 'first_name': 'Hashim',
#                 'last_name': 'Qayoom',
#                 'email': 'hashim@karmayatri.com',
#                 'phone_number': '+91 7051672720',
#                 'business_name': 'Karma Yatri',
#                 'instagram_link': 'https://www.instagram.com/karmayatri',
#                 'expertise_categories': ['Motorbike Tours'],
#                 'agent_starting_date': today - timedelta(days=18*365),
#             },
#             {
#                 'username': 'tsezin_angmo',
#                 'first_name': 'Tsezin',
#                 'last_name': 'Angmo',
#                 'email': 'hello@thejadehouse.in',
#                 'phone_number': '+91 99581 11003',
#                 'business_name': 'Jade House',
#                 'expertise_categories': ['Cultural Tours'],
#                 'agent_starting_date': today - timedelta(days=9*365),
#             },
#             {
#                 'username': 'muzammil_hussain',
#                 'first_name': 'Muzammil',
#                 'last_name': 'Hussain',
#                 'email': 'journeys@rootsladakh.in',
#                 'phone_number': '9419887776',
#                 'business_name': 'Roots Ladakh',
#                 'expertise_categories': ['Cultural Tours', 'Wildlife Tours'],
#                 'agent_starting_date': today - timedelta(days=9*365),
#             },
#         ]
        

#         for agent_data in agents_data:
#             self.stdout.write(self.style.NOTICE(f"Processing agent: {agent_data['username']}"))
#             try:
#                 with transaction.atomic():
#                     user, user_created = User.objects.get_or_create(
#                         username=agent_data['username'],
#                         defaults={
#                             'email': agent_data['email'],
#                             'first_name': agent_data['first_name'],
#                             'last_name': agent_data['last_name'],
#                             'is_agent': True,
#                             'country': 'India',
#                             'region': ladakh,
#                             'phone_number': agent_data['phone_number'],
#                         }
#                     )
                    
#                     if user_created:
#                         self.stdout.write(self.style.SUCCESS(f'Created new user: {user.username}'))
#                     else:
#                         self.stdout.write(self.style.WARNING(f'User {user.username} already existed'))
                    
#                     agent_profile, profile_created = AgentProfile.objects.update_or_create(
#                         user=user,
#                         defaults={
#                             'business_name': agent_data['business_name'],
#                             'instagram_link': agent_data.get('instagram_link'),
#                             'website': agent_data.get('website'),
#                             'hotel_owner': agent_data.get('hotel_owner', False),
#                             'join_date': today,
#                             'agent_starting_date': agent_data['agent_starting_date'],
#                         }
#                     )
                    
#                     if profile_created:
#                         self.stdout.write(self.style.SUCCESS(f'Created new agent profile for: {user.username}'))
#                     else:
#                         self.stdout.write(self.style.SUCCESS(f'Updated existing agent profile for: {user.username}'))

#                     expertise_categories = [
#                         ExpertiseCategory.objects.get_or_create(name=ec)[0] 
#                         for ec in agent_data.get('expertise_categories', [])
#                     ]
#                     agent_profile.expertise_category.set(expertise_categories)
#                     self.stdout.write(self.style.SUCCESS(f'Set expertise categories for: {user.username}'))

#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Error processing agent {agent_data["username"]}: {str(e)}'))

#         self.stdout.write(self.style.SUCCESS("Finished agent creation process"))

#     def create_external_review_sources(self):
#         sources = [
#             {"name": "booking.com", "weight": 0.6},
#             {"name": "google", "weight": 0.4},
#             {"name": "TripAdvisor", "weight": 0.5},
#         ]
#         for source in sources:
#             ExternalReviewSource.objects.get_or_create(name=source["name"], defaults={"weight": source["weight"]})
#         self.stdout.write(self.style.SUCCESS('Created external review sources'))

#     def create_tags(self):
#         tag_names = [
#             "Luxury", "Heritage Home", "Culinary Stay", "Cultural Immersion",
#             "Homestay", "Experiential", "Affordable", "Farm-to-Table",
#             "Highly Original", "Wild and Remote", "Wellbeing", "Natural Space",
#             "Environmentally Conscious", "Out of this world", "Staying with a Family"
#         ]
#         tags = {}
#         for name in tag_names:
#             tag, _ = Tag.objects.get_or_create(name=name)
#             tags[name] = tag
#         self.stdout.write(self.style.SUCCESS('Created tags'))
#         return tags

#     def create_hotels(self, tags):
#         self.stdout.write("Creating hotels...")
#         hotels_data = [
#             {
#                 "name": "The Indus River Camp",
#                 "description": "A 40-acre natural sanctuary within Ladakh's Himalayan desert",
#                 "min_price_in_INR": 13700,
#                 "type": "Mountain Stays",
#                 "google_place_id": "ChIJmzAbOAnt_TgR-_f9hVvDX3g",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Indus Valley",
#                 "hotel_owner": "nico_toller",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": True,
#                 "serves_alcohol": False,
#                 "tags": ["Heritage Home", "Cultural Immersion", "Experiential", "Farm-to-Table", "Wellbeing", "Out of this world"],
#                 "rooms": [
#                     {"name": "Riverside Cottage", "description": "The Riverside Cottages look out onto the Indus River, Shey Palace and the Ladakh range from their glass-front. <br> The showers offer a 180-degree view of the surrounding flora, with the Stok Kangri peak in the distance. <br> Each cottage has a large verandah, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br> The rooms are built primarily with sun-baked mud bricks, local wood and glass.", "size": 210, "count": 3},
#                     {"name": "Riverside Cabin", "description": "The Riverside Cabins are designed for warmth and privacy, whilst offering a view of the Indus River, Shey Palace and the Himalayan range from the bedroom. <br> Each cabin has a verandah, a writing desk, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br> The cabins are built primarily with sun-baked mud bricks, local wood and glass.", "size": 245, "count": 2},
#                     {"name": "Riverside Chalet", "description": "The Riverside Chalets (and suite) have the widest glass-front, to maximise the view, offering a view of the Indus River, Shey Palace and the Himalayan range. <br> Each chalet has a large verandah, a writing desk, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br>The rooms are built primarily with sun-baked mud bricks, local wood and glass.", "size": 360, "count": 2},
#                     {"name": "Riverside Suite", "description": "Like the Chalets, the Riverside Suite has the widest glass-front to maximise the view of the Indus River, Shey Palace and the Ladakh range. <br> The suite is the largest, most private riverside room, with an additional living room looking out onto Stok Kangri peak.", "size": 450, "count": 1},
#                     {"name": "Villa", "description": "The Villa is our largest, most secluded accommodation in our 40-acre land. It is not riverside - it's a 5 minutes walk to the river. <br> A bedroom, living room, kitchen, and bathroom make up 1,100 square feet of space. The bathroom comes with a bathtub and a washing machine. The living area has a fully equipped kitchen with a fridge. Large, comfy sofas and a dining table adorn the living space. The villa also has a roof terrace, overlooking two ponds. <br> The villa is totally off-grid, powered by solar electricity and solar water heaters.", "size": 1100, "count": 1},
#                 ]
#             },
#             {
#                 "name": "Nimmu House",
#                 "description": "A 120 year old heritage home, set in an apple and apricot orchard",
#                 "min_price_in_INR": 15800,
#                 "type": "Mountain Stays",
#                 "google_place_id": "ChIJp73RFX2Y_TgR83JsPHHS45c",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Sham Valley",
#                 "hotel_owner": "vikram_nimmu",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": False,
#                 "serves_alcohol": False,
#                 "tags": ["Experiential", "Wellbeing", "Environmentally Conscious"],
#                 "rooms": [
#                     {"name": "Heritage Room", "description": "The Heritage Rooms of Nimmu House give you the opportunity to stay in distinct, architecturally fascinating setting, with remarkable comfort", "size": 240, "count": 5},
#                     {"name": "Deluxe Tent", "description": "Nimmu House's luxurious tents are spread out between the apple and apricot orchard. Comfortable beds, a sitting area and a large bathroom", "size": 280, "count": 7},
#                 ]
#             },
#             {
#                 "name": "The Kyagar",
#                 "description": "A luxury, spacious resort with unique architecture and views",
#                 "min_price_in_INR": 23000,
#                 "type": "Mountain Stays",
#                 "google_place_id": "ChIJmzAbOAnt_TgR-_f9hVvDX3g",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Nubra Valley",
#                 "hotel_owner": "rinchen_kalon",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": False,
#                 "serves_alcohol": False,
#                 "tags": ["Luxury", "Farm-to-Table", "Natural Space", "Environmentally Conscious", "Experiential"],
#                 "rooms": [
#                     {"name": "Mountain View Suite", "description": "Kyagar's spacious suites are utterly unique - views onto the Karakoram range, a sky light view of the night sky and all built using local, traditional materials, yet with extreme comfort and style", "size": 720, "count": 16},
#                 ]
#             },
#             {
#                 "name": "Shan at Uley",
#                 "description": "A cosy winter lodge high in the mountains, in the land of the Shan (snow leopard)",
#                 "min_price_in_INR": 20000,
#                 "type": "Wildlife and Jungle Lodges",
#                 "google_place_id": "ChIJfQygJk4J_TgRdcowW2V_sNA",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Sham Valley",
#                 "hotel_owner": "morup_namgial",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": False,
#                 "serves_alcohol": False,
#                 "tags": ["Natural Space", "Environmentally Conscious", "Wild and Remote", "Experiential", "Staying with a Family"],
#                 "rooms": []  # No specific room information provided
#             },
#             {
#                 "name": "Drenmo Lodge",
#                 "description": "Tucked away in the Mushkow Valley, set in an extraordinary vantage point, Drenmo is the ultimate lodge for spotting the Himalayan Brown Bear - most viewings are visible from its own veranda",
#                 "min_price_in_INR": 25000,
#                 "type": "Wildlife and Jungle Lodges",
#                 "google_place_id": "ChIJfVYnPYqr4zgRqKQPe8zsb1o",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Mushkow Valley",
#                 "hotel_owner": "muzammil_hussain",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": False,
#                 "serves_alcohol": False,
#                 "tags": ["Natural Space", "Environmentally Conscious", "Wild and Remote", "Experiential"],
#                 "rooms": []  # No specific room information provided
#             },
#             {
#                 "name": "Jade House",
#                 "description": "A highly personal stay with a wonderful family, knowledgeable and proactive hosts in a quiet, yet central part of Leh. Comfortable rooms and superb food top it off",
#                 "min_price_in_INR": 7000,
#                 "type": "City Stay",
#                 "google_place_id": "ChIJxyhqlLfr_TgRwu399rMmR1o",
#                 "region_name": "Ladakh",
#                 "region_subsection": "Leh",
#                 "hotel_owner": "tsezin_angmo",
#                 "pet_friendly": False,
#                 "wheelchair_accessible": False,
#                 "serves_alcohol": False,
#                 "tags": ["Affordable", "Cultural Immersion", "Homestay", "Staying with a Family"],
#                 "rooms": []  # No specific room information provided
#             }
#         ]

#         for hotel_data in hotels_data:
#             try:
#                 region = Region.objects.get(name=hotel_data["region_name"])
#                 region_subsection = RegionSubsection.objects.get(name=hotel_data["region_subsection"], region=region)
                
#                 agent_profile = AgentProfile.objects.get(user__username=hotel_data["hotel_owner"])
#                 hotel_owner = agent_profile.user  # This is the User instance we need

#                 hotel, created = CustomizedHotel.objects.get_or_create(
#                     name=hotel_data["name"],
#                     defaults={
#                         "description": hotel_data["description"],
#                         "platform_hotel": True,
#                         "min_price_in_INR": hotel_data["min_price_in_INR"],
#                         "is_active": True,
#                         "type": hotel_data["type"],
#                         "google_place_id": hotel_data.get("google_place_id"),
#                         "region": region,
#                         "region_subsection": region_subsection,
#                         "hotel_owner": hotel_owner,
#                         "pet_friendly": hotel_data["pet_friendly"],
#                         "wheelchair_accessible": hotel_data["wheelchair_accessible"],
#                         "serves_alcohol": hotel_data["serves_alcohol"],
#                     }
#                 )

#                 if created:
#                     self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))
#                 else:
#                     self.stdout.write(self.style.WARNING(f'Hotel {hotel.name} already exists'))

#                 for tag_name in hotel_data["tags"]:
#                     hotel.tags.add(tags[tag_name])

#                 for room_data in hotel_data.get("rooms", []):
#                     HotelRoom.objects.get_or_create(
#                         name=room_data["name"],
#                         customized_hotel=hotel,
#                         defaults={
#                             "room_description": room_data["description"],
#                             "room_size_sq_ft": room_data["size"],
#                             "room_count": room_data["count"],
#                         }
#                     )

#             except ValidationError as e:
#                 self.stdout.write(self.style.ERROR(f'Validation error creating hotel {hotel_data["name"]}: {str(e)}'))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Error creating hotel {hotel_data["name"]}: {str(e)}'))

#     def diagnose_agent_profiles(self):
#         self.stdout.write(self.style.NOTICE("Diagnosing AgentProfiles..."))
#         for user in User.objects.filter(is_agent=True):
#             try:
#                 profile = AgentProfile.objects.get(user=user)
#                 empty_fields = []
#                 for f in AgentProfile._meta.get_fields():
#                     if f.name != 'user' and not f.is_relation:  # Skip user field and relation fields
#                         value = getattr(profile, f.name)
#                         if value in [None, '', []]:
#                             empty_fields.append(f.name)
#                 if empty_fields:
#                     self.stdout.write(self.style.WARNING(f"AgentProfile for {user.username} has empty fields: {', '.join(empty_fields)}"))
#                 else:
#                     self.stdout.write(self.style.SUCCESS(f"AgentProfile for {user.username} is complete"))
#             except AgentProfile.DoesNotExist:
#                 self.stdout.write(self.style.ERROR(f"No AgentProfile found for user {user.username}"))

# # # management/commands/populate_real_data.py
# # from django.core.management.base import BaseCommand
# # from hotels.models import CustomizedHotel, HotelRoom
# # from itineraries.models import AgentItinerary
# # from media.models import Photo
# # from customers.models import AgentProfile
# # from django.core.files import File
# # from region.models import Region, RegionSubsection
# # from common.models import Tag
# # from reviews.models import ExternalReviewSource
# # from customers.models import AgentProfile, ExpertiseCategory
# # from datetime import timedelta
# # from django.utils import timezone
# # from django.contrib.auth import get_user_model




# # User = get_user_model()



# # class Command(BaseCommand):
# #     help = 'Populate database with real hotel and itinerary data'

# #     #
# #     def handle(self, *args, **kwargs):
# #         # Create ExpertiseCategories
# #         snow_leopard_tours, _ = ExpertiseCategory.objects.get_or_create(name="Snow Leopard Tours")
# #         cultural_tours, _ = ExpertiseCategory.objects.get_or_create(name="Cultural Tours")
# #         motorbike_tours, _ = ExpertiseCategory.objects.get_or_create(name="Motorbike Tours")
# #         wildlife_tours, _ = ExpertiseCategory.objects.get_or_create(name="Wildlife Tours")


# #         # Get Ladakh region
# #         ladakh, _ = Region.objects.get_or_create(name="Ladakh")

# #         # Current date for calculations
# #         today = timezone.now().date()

# #         # Create agents
# #         agents_data = [
# #             {
# #                 'username': 'gulzar_hussain',
# #                 'first_name': 'Gulzar',
# #                 'last_name': 'Hussain',
# #                 'email': 'gulzar.stalam@gmail.com',
# #                 'phone_number': '+91 88034 25501',
# #                 'business_name': 'Frozen Himalayas',
# #                 'instagram_link': 'https://www.instagram.com/gulzar.himalayas/',
# #                 'expertise_categories': [snow_leopard_tours, cultural_tours],
# #                 'agent_starting_date': today - timedelta(days=12*365),
# #             },
# #             {
# #                 'username': 'vikram_nimmu',
# #                 'first_name': 'Vikram',
# #                 'last_name': '',
# #                 'email': 'contact@nimmu-house.com',
# #                 'phone_number': '+91 99998 45726',
# #                 'business_name': 'Nimmu House',
# #                 'hotel_owner': True,
# #                 'agent_starting_date': today - timedelta(days=15*365),
# #             },
# #             {
# #                 'username': 'morup_namgial',
# #                 'first_name': 'Morup',
# #                 'last_name': 'Namgial',
# #                 'email': 'shanatuley@gmail.com',
# #                 'phone_number': '+91 97973 44047',
# #                 'business_name': 'Shan at Uley',
# #                 'instagram_link': 'https://www.instagram.com/morup_namgail',
# #                 'hotel_owner': True,
# #                 'expertise_categories': [snow_leopard_tours],
# #                 'agent_starting_date': today - timedelta(days=7*365),
# #             },
# #             {
# #                 'username': 'rinchen_kalon',
# #                 'first_name': 'Rinchen',
# #                 'last_name': 'Kalon',
# #                 'email': 'thekyagar@gmail.com',
# #                 'phone_number': '+91 98104 27145',
# #                 'business_name': 'The Kyagar',
# #                 'hotel_owner': True,
# #                 'agent_starting_date': today - timedelta(days=15*365),
# #             },
# #             {
# #                 'username': 'nico_toller',
# #                 'first_name': 'Nico',
# #                 'last_name': 'Toller',
# #                 'email': 'theindusrivercamp@gmail.com',
# #                 'phone_number': '+91 7051379442',
# #                 'business_name': 'The Indus River Cam',
# #                 'hotel_owner': True,
# #                 'agent_starting_date': today - timedelta(days=8*365),
# #             },
# #             {
# #                 'username': 'hashim_qayoom',
# #                 'first_name': 'Hashim',
# #                 'last_name': 'Qayoom',
# #                 'email': 'hashim@karmayatri.com',
# #                 'phone_number': '+91 7051672720',
# #                 'business_name': 'Karma Yatri',
# #                 'instagram_link': 'https://www.instagram.com/karmayatri',
# #                 'expertise_categories': [motorbike_tours],
# #                 'agent_starting_date': today - timedelta(days=18*365),
# #             },
# #             {
# #                 'username': 'tsezin_angmo',
# #                 'first_name': 'Tsezin',
# #                 'last_name': 'Angmo',
# #                 'email': 'hello@thejadehouse.in',
# #                 'phone_number': '+91 99581 11003',
# #                 'business_name': 'Jade House',
# #                 'expertise_categories': [cultural_tours],
# #                 'agent_starting_date': today - timedelta(days=9*365),
# #             },
# #             {
# #                 'username': 'muzammil_hussain',
# #                 'first_name': 'Muzammil',
# #                 'last_name': 'Hussain',
# #                 'email': 'journeys@rootsladakh.in',
# #                 'phone_number': '9419887776',
# #                 'business_name': 'Roots Ladakh',
# #                 'expertise_categories': [cultural_tours, wildlife_tours],
# #                 'agent_starting_date': today - timedelta(days=9*365),
# #             },
# #         ]

# #         for agent_data in agents_data:
# #             expertise_categories = agent_data.pop('expertise_categories', [])
# #             user = User.objects.create_user(
# #                 username=agent_data['username'],
# #                 email=agent_data['email'],
# #                 first_name=agent_data['first_name'],
# #                 last_name=agent_data['last_name'],
# #                 is_agent=True,
# #                 country='India',
# #                 region=ladakh,
# #                 phone_number=agent_data['phone_number'],
# #             )
            
# #             agent_profile = AgentProfile.objects.create(
# #                 user=user,
# #                 business_name=agent_data['business_name'],
# #                 instagram_link=agent_data.get('instagram_link'),
# #                 website=agent_data.get('website'),
# #                 hotel_owner=agent_data.get('hotel_owner', False),
# #                 join_date=today,
# #                 agent_starting_date=agent_data['agent_starting_date'],
# #             )
            
# #             agent_profile.expertise_category.set(expertise_categories) 
 
 
# #         ExternalReviewSource.objects.create(weight=0.6, name="booking.com")
# #         ExternalReviewSource.objects.create(weight=0.4, name="google")
# #         ExternalReviewSource.objects.create(weight=0.5, name="TripAdvisor")
        
# #         region_subsections = {
# #             'Ladakh': [
# #                 'Nubra Valley', 'Sham Valley', 'Leh', 'Indus Valley', 
# #                 'Pangong Lake', 'Tso Moriri Lake', 'Changtang', 'Hanle', 
# #                 'Zanskar Valley', 'Markha Valley', 'Kargil', 'Mushkow Valley'
# #             ],
# #             # Add other regions and their subsections here
# #         }

# #         for region_name, subsections in region_subsections.items():
# #             region = Region.objects.get(name=region_name)
# #             for subsection_name in subsections:
# #                 RegionSubsection.objects.get_or_create(
# #                     name=subsection_name,
# #                     region=region
# #                 )


# #         tag_names = [
# #             "Luxury", "Heritage Home", "Culinary Stay", "Cultural Immersion",
# #             "Homestay", "Experiential", "Affordable", "Farm-to-Table",
# #             "Highly Original", "Wild and Remote", "Wellbeing", "Natural Space",
# #             "Environmentally Conscious", "Out of this world", "Staying with a Family"
# #         ]
# #         tags = {name: Tag.objects.create(name=name) for name in tag_names}

 
# #         # Create hotel
# #         hotel = CustomizedHotel.objects.create(
# #             name="The Indus River Camp",
# #             description="A 40-acre natural sanctuary within Ladakh's Himalayan desert",
# #             platform_hotel=True,
# #             min_price_in_INR=13700,
# #             is_active=True,
# #             type="Mountain Stays",
# #             google_place_id="ChIJmzAbOAnt_TgR-_f9hVvDX3g",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Indus Valley', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='nico_toller'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = True,
# #             serves_alcohol = False
# #         )

# #         # Add specific tags to the hotel
# #         hotel.tags.add(
# #             tags["Heritage Home"],
# #             tags["Cultural Immersion"],
# #             tags["Experiential"],
# #             tags["Farm-to-Table"],
# #             tags["Welbeing"],
# #             tags["Out of this World"]

# #         )

# #         HotelRoom.objects.create(
# #             name="Riverside Cottage",
# #             room_description="The Riverside Cottages look out onto the Indus River, Shey Palace and the Ladakh range from their glass-front. <br> The showers offer a 180-degree view of the surrounding flora, with the Stok Kangri peak in the distance. <br> Each cottage has a large verandah, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br> The rooms are built primarily with sun-baked mud bricks, local wood and glass.",
# #             customized_hotel=hotel,
# #             room_size_sq_ft=210,
# #             room_count=3
# #         )

# #         HotelRoom.objects.create(
# #             name="Riverside Cabin",
# #             room_description="The Riverside Cabins are designed for warmth and privacy, whilst offering a view of the Indus River, Shey Palace and the Himalayan range from the bedroom. <br> Each cabin has a verandah, a writing desk, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br> The cabins are built primarily with sun-baked mud bricks, local wood and glass.",
# #             customized_hotel=hotel,
# #             room_size_sq_ft=245,
# #             room_count=2
# #         )

# #         HotelRoom.objects.create(
# #             name="Riverside Chalet",
# #             room_description="The Riverside Chalets (and suite) have the widest glass-front, to maximise the view, offering a view of the Indus River, Shey Palace and the Himalayan range. <br> Each chalet has a large verandah, a writing desk, a king-size bed with high-quality bed linen and Rajasthani quilts and eco-conscious hotel amenities. <br>The rooms are built primarily with sun-baked mud bricks, local wood and glass.",
# #             customized_hotel=hotel,
# #             room_size_sq_ft=360,
# #             room_count=2
# #         )

# #         HotelRoom.objects.create(
# #             name="Riverside Suite",
# #             room_description="Like the Chalets, the Riverside Suite has the widest glass-front to maximise the view of the Indus River, Shey Palace and the Ladakh range. <br> The suite is the largest, most private riverside room, with an additional living room looking out onto Stok Kangri peak. ",
# #             customized_hotel=hotel, 
# #             room_size_sq_ft=450,
# #             room_count=1
# #         )

# #         HotelRoom.objects.create(
# #             name="Villa",
# #             room_description="The Villa is our largest, most secluded accommodation in our 40-acre land. It is not riverside - it's a 5 minutes walk to the river. <br> A bedroom, living room, kitchen, and bathroom make up 1,100 square feet of space. The bathroom comes with a bathtub and a washing machine. The living area has a fully equipped kitchen with a fridge. Large, comfy sofas and a dining table adorn the living space. The villa also has a roof terrace, overlooking two ponds. <br> The villa is totally off-grid, powered by solar electricity and solar water heaters.",
# #             customized_hotel=hotel,
# #             room_size_sq_ft=1100,
# #             room_count=1
# #         )

# #         hotel2 = CustomizedHotel.objects.create(
# #             name="Nimmu House",
# #             description="A 120 year old heritage home, set in an apple and apricot orchard",
# #             platform_hotel=True,
# #             min_price_in_INR=15800,
# #             is_active=True,
# #             type="Mountain Stays",
# #             google_place_id="ChIJp73RFX2Y_TgR83JsPHHS45c",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Sham Valley', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='vikram_nimmu'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = False,
# #             serves_alcohol = False
# #         )

# #         # Add specific tags to the hotel
# #         hotel2.tags.add(
# #             tags["Experiential"],
# #             tags["Unique"],
# #             tags["Wellbeing"],
# #             tags["Environmentally Conscious"],

# #         )


# #         HotelRoom.objects.create(
# #             name="Heritage Room",
# #             room_description=" The Heritage Rooms of Nimmu House give you the opportunity to stay in distinct, architecturally fascinating setting, with remarkable comfort",
# #             customized_hotel=hotel2, 
# #             room_size_sq_ft=240,
# #             room_count=5
# #         )

# #         HotelRoom.objects.create(
# #             name="Deluxe Tent",
# #             room_description="Nimmu House's luxurious tents are spread out between the apple and apricot orchard. Comfortable beds, a sitting area and a large bathroom",
# #             customized_hotel=hotel2,
# #             room_size_sq_ft=280,
# #             room_count=7,
# #         )


# #         hotel3 = CustomizedHotel.objects.create(
# #             name="The Kyagar",
# #             description="A luxury, spacious resort with unique architecture and views",
# #             platform_hotel=True,
# #             min_price_in_INR=23000,
# #             is_active=True,
# #             type="Mountain Stays",
# #             google_place_id="ChIJmzAbOAnt_TgR-_f9hVvDX3g",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Nubra Valley', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='rinchen_kalon'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = False,
# #             serves_alcohol = False
# #         )


# #         hotel3.tags.add(
# #             tags["Luxury"],
# #             tags["Farm-to-Table"],
# #             tags["Natural Space"],
# #             tags["Environmentally Conscious"],
# #             tags["Experiential"]

# #         )

# #         HotelRoom.objects.create(
# #             name="Mountain View Suite",
# #             room_description="Kyagar's spacious suites are utterly unique - views onto the Karakoram range, a sky light view of the night sky and all built using local, traditional materials, yet with extreme comfort and style",
# #             customized_hotel=hotel3,
# #             room_size_sq_ft=720,
# #             room_count=16,
# #         )

# #         hotel4 = CustomizedHotel.objects.create(
# #             name="Shan at Uley - A Snow Leopard Lodge",
# #             description="A cosy winter lodge high in the mountains, in the land of the Shan (snow leopard)",
# #             platform_hotel=True,
# #             min_price_in_INR=20000,
# #             is_active=True,
# #             type="Wildlife and Jungle Lodges",
# #             google_place_id="ChIJfQygJk4J_TgRdcowW2V_sNA",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Sham Valley', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='morup_namgial'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = False,
# #             serves_alcohol = False
# #         )


# #         hotel4.tags.add(
# #             tags["Natural Space"],
# #             tags["Environmentally Conscious"],
# #             tags["Wild and Remote"],
# #             tags["Experiential"],
# #             tags["Staying with a Family"]     
# #         )


# #         hotel5 = CustomizedHotel.objects.create(
# #             name="Drenmo - A Himalayan Brown Bear Lodge",
# #             description="Tucked away in the Mushkow Valley, set in an extraordinary vantage point, Drenmo is the ultimate lodge for spotting the Himalayan Brown Bear - most viewings are visible from its own veranda",
# #             platform_hotel=True,
# #             min_price_in_INR=25000,
# #             is_active=True,
# #             type="Wildlife and Jungle Lodges",
# #             google_place_id="ChIJfVYnPYqr4zgRqKQPe8zsb1o",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Mushkow Valley', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='muzammil_hussain'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = False,
# #             serves_alcohol = False,
# #         )


# #         hotel5.tags.add(
# #             tags["Natural Space"],
# #             tags["Environmentally Conscious"],
# #             tags["Wild and Remote"],
# #             tags["Experiential"],
# #         )
        

# #         # Add specific tags to the hotel


# #         hotel6 = CustomizedHotel.objects.create(
# #             name="Jade House",
# #             description="A highly personal stay with a wonderful family, knowledgeable and proactive hosts in a quiet, yet central part of Leh. Comfortable rooms and superb food top it off ",
# #             platform_hotel=True,
# #             min_price_in_INR=7000,
# #             is_active=True,
# #             type="City Stay",
# #             google_place_id="ChIJxyhqlLfr_TgRwu399rMmR1o",
# #             region=Region.objects.get(id=14),
# #             region_subsection=RegionSubsection.objects.get(name='Leh', region__name='Ladakh'),
# #             hotel_owner = AgentProfile.objects.get(user_username='tsezin_angmo'),
# #             pet_friendly = False, 
# #             wheelchair_accessible = False,
# #             serves_alcohol = False
# #         )


# #         hotel6.tags.add(
# #             tags["Affordable"],
# #             tags["Cultural Immersion"],
# #             tags["Homestay"],
# #             tags["Staying with a Family"]
# #         )


# #         self.stdout.write(self.style.SUCCESS('Successfully populated database with real data'))



# #         # # Create itineraries
# #         # itinerary1 = AgentItinerary.objects.create(
# #         #     name="City Explorer",
# #         #     description="Explore the vibrant city life",
# #         #     cost_for_1_pax=10000,
# #         #     type="Cultural",
# #         #     agent=agent1
# #         # )
# #         # # Add more itineraries...

# #         # # Add photos
# #         # with open('path/to/hotel1_photo.jpg', 'rb') as img_file:
# #         #     Photo.objects.create(hotel=hotel1, image=File(img_file))

# #         # with open('path/to/itinerary1_photo.jpg', 'rb') as img_file:
# #         #     Photo.objects.create(itinerary=itinerary1, image=File(img_file))

# #         # # Add more photos...
