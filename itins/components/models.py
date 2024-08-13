from django.db import models
from django.conf import settings
from contacts.models import Contact
from hotels.models import HotelRoom

class ComponentType(models.Model):
    name = models.CharField(max_length=100)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_global = models.BooleanField(default=False)
    is_deletable = models.BooleanField(default=True)  # Hotel room type can have this as False

    def __str__(self):
        return self.name

class Component(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('ironman', 'Ironman'),    
        ('tough', 'Tough'),
        ('challenging', 'Challenging'),
        ('moderate', 'Moderate'),
        ('easy', 'Easy'),
    ]

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    component_type = models.ForeignKey(ComponentType, on_delete=models.SET_NULL, blank=True, null=True)
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_platform_experience = models.BooleanField(default=False)
    # platform experience would be like urbanaut experiences
    is_visible_to_all = models.BooleanField(default=False)
    
    wheelchair_accessible = models.BooleanField(default=True, blank=True, null=True)
    age_limit = models.PositiveIntegerField(blank=True, null=True)
    fitness_level = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='all', blank=True, null=True)
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    price_for_1_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_for_2_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_for_3_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_for_4_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fixed_price_overall = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fixed_price_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    net_price_for_1_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price_for_2_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price_for_3_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price_for_4_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_fixed_price_overall = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_fixed_price_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.name
# This function allows a component to be passed from one agent to the next
    
# Usage example:
    
# # Assume you have a component instance and a new agent instance
# original_component = Component.objects.get(id=component_id)
# new_agent = Agent.objects.get(id=new_agent_id)

# # Transfer the component to the new agent
# new_component = original_component.transfer_to_agent(new_agent)

    def transfer_to_agent(self, new_agent):
        new_component = Component.objects.create(
            agent=new_agent,
            name=self.name,
            description=self.description,
            component_type=self.component_type,
            hotel_room=self.hotel_room,
            is_platform_experience=self.is_platform_experience,
            is_visible_to_all=self.is_visible_to_all,
            wheelchair_accessible=self.wheelchair_accessible,
            age_limit=self.age_limit,
            fitness_level=self.fitness_level,
            contact=self.contact,
            price_for_1_pax=self.price_for_1_pax,
            price_for_2_pax=self.price_for_2_pax,
            price_for_3_pax=self.price_for_3_pax,
            price_for_4_pax=self.price_for_4_pax,
            fixed_price_overall=self.fixed_price_overall,
            fixed_price_per_person=self.fixed_price_per_person
        )
        return new_component




# The below function allows to create a component for a list of agents - identical infromation, except for the agent field, but newisntance. The following two lines are the usage
# agents = Agent.objects.filter(conditions)  # Get a list of agents
# new_components = Component.create_for_agents(agents, field1=value1, field2=value2)
# This is how we can get a list of Ladakhi agents the taxi components

    @classmethod
    def create_for_agents(cls, agents, **kwargs):
        new_components = []
        for agent in agents:
            new_component = cls(agent=agent, **kwargs)
            new_component.save()
            new_components.append(new_component)
        return new_components

    def __str__(self):
        return self.name