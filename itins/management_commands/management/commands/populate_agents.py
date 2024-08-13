# populate_agents.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from customers.models import AgentProfile, ExpertiseCategory
from region.models import Region

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with agent data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting agent population...'))

        # Get or create the Ladakh region
        ladakh, _ = Region.objects.get_or_create(name="Ladakh")

        # Current date for calculations
        today = timezone.now().date()

        # Agent data
        agents_data = [
            {
                'username': 'example_agent',
                'email': 'example@example.com',
                'first_name': 'Example',
                'last_name': 'Agent',
                'phone_number': '+91 1234567890',
                'business_name': 'Example Business',
                'instagram_link': 'https://www.instagram.com/example',
                'website': 'https://www.example.com',
                'expertise_categories': ['Example Category 1', 'Example Category 2'],
                'agent_starting_date': today - timedelta(days=5*365),  # 5 years ago
                'hotel_owner': False,
            },
            # Add more agent data dictionaries here
        ]

        self.create_agents(agents_data, ladakh)

        self.stdout.write(self.style.SUCCESS('Finished populating agents'))

    def create_agents(self, agents_data, region):
        for agent_data in agents_data:
            self.stdout.write(self.style.NOTICE(f"Processing agent: {agent_data['username']}"))
            try:
                with transaction.atomic():
                    user, user_created = User.objects.update_or_create(
                        username=agent_data['username'],
                        defaults={
                            'email': agent_data['email'],
                            'first_name': agent_data['first_name'],
                            'last_name': agent_data['last_name'],
                            'is_agent': True,
                            'country': 'India',
                            'region': region,
                            'phone_number': agent_data['phone_number'],
                        }
                    )
                    
                    if user_created:
                        self.stdout.write(self.style.SUCCESS(f'Created new user: {user.username}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated existing user: {user.username}'))
                    
                    agent_profile, profile_created = AgentProfile.objects.update_or_create(
                        user=user,
                        defaults={
                            'business_name': agent_data['business_name'],
                            'instagram_link': agent_data.get('instagram_link'),
                            'website': agent_data.get('website'),
                            'hotel_owner': agent_data.get('hotel_owner', False),
                            'join_date': timezone.now().date(),
                            'agent_starting_date': agent_data['agent_starting_date'],
                        }
                    )
                    
                    if profile_created:
                        self.stdout.write(self.style.SUCCESS(f'Created new agent profile for: {user.username}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated existing agent profile for: {user.username}'))

                    expertise_categories = [
                        ExpertiseCategory.objects.get_or_create(name=ec)[0] 
                        for ec in agent_data.get('expertise_categories', [])
                    ]
                    agent_profile.expertise_category.set(expertise_categories)
                    self.stdout.write(self.style.SUCCESS(f'Set expertise categories for: {user.username}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing agent {agent_data["username"]}: {str(e)}'))