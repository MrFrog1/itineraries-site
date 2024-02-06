from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps


class ExpertiseCategory(models.Model):
    name = models.CharField(max_length=100)


class Agent(AbstractUser):
    phone_number = models.CharField(max_length=50)
    email_address = models.EmailField()
    region = models.CharField(max_length=100)
    bio = models.TextField(max_length=450)
    public_profile = models.BooleanField(default=True)
    expertise_category = models.ManyToManyField(ExpertiseCategory)  # Assuming you'll define this elsewhere
    hotel_owner = models.BooleanField(default=False)
    paired_with_other_agent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField()
    nickname = models.CharField(max_length=50)
    agent_starting_date = models.DateField(null=True, blank=True) # This is the date the agent started working, so we can calculate their experience

    admin_description = models.TextField(max_length=450, blank=True, null=True)

    default_commission_percentage = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    default_organisation_fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='agent_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='agent_permissions',
        blank=True
    )

class InterestCategory(models.Model):
    name = models.CharField(max_length=100)
    # Other fields you may need for the category
 

class Customer(AbstractUser):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)

    blocked_agents = models.ManyToManyField('Agent', blank=True, through='BlockedAgent')

    phone_number = models.CharField(max_length=50)
    email_address = models.EmailField()
    public_profile = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    interests = models.ManyToManyField(InterestCategory)  # Assuming you'll define this elsewhere

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_permissions',
        blank=True
    )

    def block_agent(self, agent):
        BlockedAgent.objects.get_or_create(customer=self, agent=agent)

    def is_agent_blocked(self, agent):
        return BlockedAgent.objects.filter(customer=self, agent=agent).exists()

    def has_blocked(self, agent):
        return self.blocked_agents.filter(id=agent.id).exists()

    def has_interacted_with(self, agent):
        # Dynamically retrieve the CustomerItinerary model
        CustomerItinerary = apps.get_model('itineraries', 'CustomerItinerary')
        # Check for shared itineraries
        itineraries_exist = CustomerItinerary.objects.filter(customer=self, agent=agent).exists()

# Once messaging is sorted, replace this with the following:

        # # Dynamically retrieve the Message model (replace 'app_name' with the actual app name where Message model is located)
        # Message = apps.get_model('app_name', 'Message')
        # # Check for messages exchanged
        # messages_exist = Message.objects.filter(sender=self.user, recipient=agent.user).exists() or \
        #                  Message.objects.filter(sender=agent.user, recipient=self.user).exists()

        return itineraries_exist #or messages_exist
    
class BlockedAgent(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_blocked_agents')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['customer', 'agent']

    def __str__(self):
        return f"{self.customer.user.username} blocked {self.agent.user.username}"