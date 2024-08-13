from django.db import models
from django.conf import settings
from contacts.models import Contact
from hotels.models import HotelRoom



# A Component can be a hotel, a taxi, a guide, a restaurant, etc

# A component can depend on a Contact? Or it can be from a category list?
# HAVE GLOBAL COMPONENTS THAT ANYONE CAN ACCESS

class ComponentType(models.Model):
    name = models.CharField(max_length=100)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_deletable = models.BooleanField(default=True)  # Hotel room type can have this as False

    def __str__(self):
        return self.name

# This property is for global types that can't be removed by the agent
    @property
    def is_global_type(self):
        return self.agent is None
    


CATEGORY_CHOICES = [
    ('all', 'All'),
    ('ironman', 'Ironman'),    
    ('tough', 'Tough'),
    ('challenging', 'Challenging'),
    ('moderate', 'moderate'),
    ('easy', 'Easy'),

]


class Component(models.Model):

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()

# Restrictions
    wheelchair_accessible= models.BooleanField(default=True)
    age_limit = models.PositiveIntegerField(blank=True, null=True)
    fitness_level = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='all')
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
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
            contact=self.contact,
            price_for_1_pax=self.price_for_1_pax,
            price_for_2_pax=self.price_for_2_pax,
            price_for_3_pax=self.price_for_3_pax,
            price_for_4_pax=self.price_for_4_pax,
            fixed_price_overall=self.fixed_price_overall,
            fixed_price_per_person=self.fixed_price_per_person,
            net_price_for_1_pax=self.price_for_1_pax,
            net_price_for_2_pax=self.price_for_2_pax,
            net_price_for_3_pax=self.price_for_3_pax,
            net_price_for_4_pax=self.price_for_4_pax,
            net_fixed_price_overall=self.fixed_price_overall,
            net_fixed_price_per_person=self.fixed_price_per_person
        )
        return new_component
    


# The below function allows to create a component for a list of agents - identical infromation, except for the agent field, but newisntance. The following two lines are the usage
# agents = Agent.objects.filter(conditions)  # Get a list of agents
# new_components = Component.create_for_agents(agents, field1=value1, field2=value2)
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
    

