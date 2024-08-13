from django.db import models, transaction
from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError
from django.db import models
from django.contrib.auth.models import AbstractUser
from region.models import Region

class User(AbstractUser):
    # Common fields
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=55, blank=True, null=True)
    public_profile = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    # Role-based fields
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=  False)


    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.is_agent:
            UserAgent.objects.create(user=self)

            
    @property
    def agent_profile(self):
        if self.is_agent:
            return self.useragent if hasattr(self, 'useragent') else None
        return None
    def has_interacted_with(self, other_user):
        # Dynamically import the Message and CustomerItinerary models
        Message = apps.get_model('messages_user', 'Message')
        CustomerItinerary = apps.get_model('itineraries', 'CustomerItinerary')
        
        if self.is_customer:
            messages_sent_to_agent = Message.objects.filter(sender=self, recipient=other_user).exists()
            if messages_sent_to_agent:
                return True
        
            shared_itinerary = CustomerItinerary.objects.filter(customer=self, agent=other_user).exists()
            if shared_itinerary:
                return True

class ExpertiseCategory(models.Model):
    name = models.CharField(max_length=100)

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_agent_profile')
    short_bio = models.TextField(max_length=155, blank=True, null=True)
    bio = models.TextField(max_length=450, blank=True, null=True)
    business_name = models.CharField(max_length=55, blank=True, null=True)
    expertise_categories = models.ManyToManyField(ExpertiseCategory, blank=True)
    website = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    sustainability_practices = models.TextField(blank=True, null=True)
    hotel_owner = models.BooleanField(default=False)
    accompanying_agent  = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    agent_starting_date = models.DateField(null=True, blank=True)  # For calculating experience
    admin_description = models.TextField(max_length=450, blank=True, null=True)
    default_commission_percentage = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    default_organisation_fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        abstract = True
    def __str__(self):
        return f"Agent Profile for {self.user.username}"

        
class UserAgent(AgentProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_agent')


class PotentialAgent(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    short_bio = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    business_name = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    expertise_categories = models.ManyToManyField(ExpertiseCategory, blank=True)
    hotel_owner = models.BooleanField(default=False)
    admin_description = models.TextField(null=True, blank=True)


# THIS ALLOWS US TO CONVERT A POTENTIAL AGENT - OR A NON-USER AGENT INTO AN AGENT BY ADDING A USERNAME AND A APSSWORD
    @transaction.atomic
    def convert_to_user(self, username, password):
        if self.is_converted:
            return None

        user = User.objects.create_user(
            username=username,
            password=password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_agent=True
        )

        user_agent = UserAgent.objects.create(
            user=user,
            short_bio=self.short_bio,
            bio=self.bio,
            business_name=self.business_name,
            website=self.website,
            instagram_link=self.instagram_link,
            sustainability_practices=self.sustainability_practices,
            hotel_owner=self.hotel_owner,
            default_commission_percentage=self.default_commission_percentage,
            default_organisation_fee=self.default_organisation_fee,
            admin_description=self.admin_description
        )

        # Transfer expertise categories
        user_agent.expertise_categories.set(self.expertise_categories.all())

        # Handle accompanying agent
        if self.accompanying_agent:
            if self.accompanying_agent.is_converted:
                user_agent.accompanying_agent = self.accompanying_agent.converted_user.user_agent
            else:
                # You might want to handle this case differently
                pass

        user_agent.save()

        self.is_converted = True
        self.converted_user = user
        self.save()

        return user

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new object
            # Set default values for fields that are in UserAgent but not in PotentialAgent
            self.public_profile = False  # Or whatever default you want
        super().save(*args, **kwargs)


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    interests = models.ManyToManyField(InterestCategory, blank=True)

    def block_agent(self, agent):
        BlockedAgent.objects.get_or_create(customer=self.user, agent=agent)

    def is_agent_blocked(self, agent):
        return BlockedAgent.objects.filter(customer=self.user, agent=agent).exists()

    def has_blocked(self, agent):
        return self.blocked_agents.filter(id=agent.id).exists()



class BlockedAgent(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_blockings')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_blockings')
    
    class Meta:
        unique_together = ['customer', 'agent']

    def __str__(self):
        return f"{self.customer.username} blocked {self.agent.username}"
    


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if instance.is_customer:
        # Use get_or_create to avoid creating a duplicate profile
         CustomerProfile.objects.update_or_create(user=instance, defaults={...})
    if instance.is_agent:
        # Use get_or_create to avoid creating a duplicate profile
        try:
            UserAgent.objects.get_or_create(user=instance)
        except IntegrityError:
            # UserAgent already exists, you might want to update it
           user_agent = UserAgent.objects.get(user=instance)

    # If the user already exists and is being saved (not created), this ensures the profile is also saved.
    # It's helpful in scenarios where the profile exists but needs to be updated based on changes to the User instance.
    if not created:
        if instance.is_customer:
            instance.customer_profile.save()
        if instance.is_agent:
            instance.agent_profile.save()