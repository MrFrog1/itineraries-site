from django.db import models
from django.conf import settings
from contacts.models import Contact
from region.models import Region
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
# from modeltranslation.translator import register, TranslationOptions (Is Creating an error with AppRegistry. Get this fixed)
from django.contrib.auth import get_user_model

User = get_user_model()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    # Platform Hotel is whether it's one that we would recommend on our platform, or one whose details are useful for agents to have, like Grand Dragon
    platform_hotel = models.BooleanField(default=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    rating = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Having both Google Place and Long/Lat allows for us to choose a different API for the map location
    google_place_id = models.CharField(max_length=255, null=True, blank=True)
    
# Min Price so can say 'Starting Price from... per night' Can calcyulate
    min_price_in_INR = models.DecimalField(max_digits=9, decimal_places=2, null=True, validators=[MinValueValidator(0)])

    is_active = models.BooleanField(default=True)  # Field to indicate if the hotel is active

    # If a hotel decides to remove itself from the platform, this is what happens
    def soft_delete(self):
        self.is_active = False
        self.save()


class PaymentType(models.Model):
    PAYMENT_CHOICES = [
        ('paytm', 'PayTM'),
        ('gpay', 'Gpay'),
        ('upi', 'UPI'),
        ('net_transfer', 'Net Transfer'),
        ('cash', 'Cash'),
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'Amex'),
    ]

    type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_type_display()

class CustomizedHotel(Hotel):

    hotel_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_customized_hotels')
    instagram_link = models.URLField(null=True, blank=True)
    pet_friendly = models.BooleanField(default=False)
    wheelchair_accessible = models.BooleanField(default=False)
        
    payment_types = models.ManyToManyField(PaymentType, blank=True)
    private_info = models.CharField(max_length=155, null=True, blank=True)
    serves_alcohol = models.BooleanField(default=False)


    def __str__(self):
        return f"Owner Customized - {self.name}"

    def soft_delete(self):
        self.is_active = False
        self.save()

    
class AgentHotel(Hotel):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customized_hotels')
    parent_hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_hotels')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    tac_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Commission percentage for this hotel")

    def create_from_existing_hotel(cls, user_id, hotel_id):
        agent = User.objects.get(id=user_id)
        parent_hotel = Hotel.objects.filter(id=hotel_id, is_active=True).first()
    
        if not parent_hotel:
            raise ValidationError("In Order To Create Your Own Hotel Instance, It Must Align with an Existing Hotel.")


        customized_hotel = cls.objects.create(
            agent=agent,
            parent_hotel=parent_hotel,
            name=parent_hotel.name,
            description=parent_hotel.description,
            primary_contact=parent_hotel.primary_contact,
            # Copy other relevant fields from the parent Hotel instance
        )

        return customized_hotel
    # Add any other fields specific to customized hotels



class HotelRoom(models.Model):
    name = models.CharField(max_length=40)
    room_description = models.CharField(max_length=100)
    
    # Relationship with CustomizedHotel
    customized_hotel = models.ForeignKey(CustomizedHotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotel_rooms')

    # Relationship with AgentHotel
    agent_hotel = models.ForeignKey(AgentHotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_hotel_rooms')

    room_count = models.IntegerField(default=1)
    
    @classmethod
    def import_from_customized_hotel(cls, agent_hotel_id, customized_hotel_room_id, agent_id):
        agent_hotel = AgentHotel.objects.filter(id=agent_hotel_id, agent_id=agent_id, is_active=True).first()
        customized_hotel_room = HotelRoom.objects.filter(id=customized_hotel_room_id, customized_hotel__hotel_owner_id=agent_id, customized_hotel__is_active=True).first()

        if not agent_hotel or not customized_hotel_room:
            raise ValidationError("Both AgentHotel and CustomizedHotelRoom instances must exist and be active.")

        # Create a new HotelRoom for the AgentHotel
        new_agent_hotel_room = cls.objects.create(
            name=customized_hotel_room.name,
            room_description=customized_hotel_room.room_description,
            agent_hotel=agent_hotel,
            room_count=customized_hotel_room.room_count
        )

        # Copy RoomPrice information from CustomizedHotel's room
        for room_price in customized_hotel_room.roomprice_set.all():
            RoomPrice.objects.create(
                hotel_room=new_agent_hotel_room,
                agent=agent_hotel.agent,
                meal_plan=room_price.meal_plan,
                rack_price_1p=room_price.rack_price_1p,
                rack_price_2p=room_price.rack_price_2p,
                rack_price_3p=room_price.rack_price_3p,
                rack_price_2p_child=room_price.rack_price_2p_child,
                rack_price_4p=room_price.rack_price_4p,
                rack_price_3p_child =room_price.rack_price_3p_child,
                rack_price_4p_child = room_price.rack_price_4p_child

            )

        # Calculate the net rates and customer rates for the new room prices
        for room_price in new_agent_hotel_room.roomprice_set.all():
            room_price.calculate_net_rates()
            room_price.calculate_customer_rates()

        return new_agent_hotel_room


    def __str__(self):
        if self.customized_hotel:
            return f"{self.customized_hotel.name} - {self.name}"
        elif self.agent_hotel:
            return f"{self.agent_hotel.name} - {self.name}"
        else:
            return self.name

    def clean(self):
        # Ensure that the room is associated with either a CustomizedHotel or an AgentHotel, but not both
        if self.customized_hotel and self.agent_hotel:
            raise ValidationError("A HotelRoom cannot be associated with both a CustomizedHotel and an AgentHotel simultaneously.")

        if not self.customized_hotel and not self.agent_hotel:
            raise ValidationError("A HotelRoom must be associated with either a CustomizedHotel or an AgentHotel.")


# Remember that clean method is not called automatically when you save an object. You have to call it explicitly in your save method 
# (as shown above) or in your forms if you are using Django forms.

    def save(self, *args, **kwargs):
        self.clean()
        super(HotelRoom, self).save(*args, **kwargs)
        


# How are we going to do seasonal rates?

class RoomPrice(models.Model):
    MEAL_PLAN_CHOICES = [
        ('EP', 'European Plan - No meals'),
        ('CP', 'Continental Plan - With breakfast'),
        ('MAP', 'Modified American Plan - With breakfast and dinner'),
        ('AP', 'American Plan - With all meals'),
    ]
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal_plan = models.CharField(max_length=100, choices=MEAL_PLAN_CHOICES)

    # Rack rates (before commission)
    rack_price_1p = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_2p = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_3p = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_2p_child = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_4p = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_3p_child = models.DecimalField(max_digits=10, decimal_places=2)
    rack_price_4p_child = models.DecimalField(max_digits=10, decimal_places=2)

    # Overridden net rates
    overridden_net_price_1p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_2p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_3p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_2p_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_4p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_3p_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overridden_net_price_4p_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    # Rates for customers
    rate_for_customer_1p = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_2p = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_3p = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_2p_child = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_4p = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_3p_child = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    rate_for_customer_4p_child = models.DecimalField(max_digits=10, decimal_places=2, editable=False)


    def calculate_net_rates(self):
        # Get the tac_percentage from the agent's hotel
        tac_percentage = self.agent.agenthotel.tac_percentage or 0

        # Calculate the net prices using the tac_percentage
        self.overridden_net_price_1p = self.rack_price_1p * (1 - tac_percentage / 100) if self.rack_price_1p else None
        self.overridden_net_price_2p = self.rack_price_2p * (1 - tac_percentage / 100) if self.rack_price_2p else None
        self.overridden_net_price_3p = self.rack_price_3p * (1 - tac_percentage / 100) if self.rack_price_3p else None
        self.overridden_net_price_2p_child = self.rack_price_2p_child * (1 - tac_percentage / 100) if self.rack_price_2p_child else None
        self.overridden_net_price_4p = self.rack_price_4p * (1 - tac_percentage / 100) if self.rack_price_4p else None
        self.overridden_net_price_3p_child = self.rack_price_3p_child * (1 - tac_percentage / 100) if self.rack_price_3p_child else None
        self.overridden_net_price_4p_child = self.rack_price_4p_child * (1 - tac_percentage / 100) if self.rack_price_4p_child else None

        self.save()


    def calculate_customer_rates(self):
        # This method calculates net rates without considering overrides

        tac_percentage = self.agent.tac_percentage if self.agent.tac_percentage else 0
        default_commission_percentage = self.agent.default_commission_percentage if self.agent.default_commission_percentage else 0

        self.rate_for_customer_1p = self.rack_price_1p - (self.rack_price_1p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_2p = self.rack_price_2p - (self.rack_price_2p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_3p = self.rack_price_3p - (self.rack_price_3p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_2p_child = self.rack_price_2p_child - (self.rack_price_2p_child * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_4p = self.rack_price_4p - (self.rack_price_4p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_3p_child = self.rack_price_3p_child - (self.rack_price_3p_child * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_4p_child = self.rack_price_4p_child - (self.rack_price_4p_child * tac_percentage * default_commission_percentage / 10000)

        self.save()

    def calculate_customer_rates_with_override(self):
        # This method calculates net rates, considering any overridden values
        tac_percentage = self.agent.tac_percentage if self.agent.tac_percentage else 0
        default_commission_percentage = self.agent.default_commission_percentage if self.agent.default_commission_percentage else 0

        # Calculate rates for each occupancy type, considering overrides if they exist
        self.rate_for_customer_1p = self.overridden_net_price_1p if self.overridden_net_price_1p is not None else self.rack_price_1p - (self.rack_price_1p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_2p = self.overridden_net_price_2p if self.overridden_net_price_2p is not None else self.rack_price_2p - (self.rack_price_2p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_3p = self.overridden_net_price_3p if self.overridden_net_price_3p is not None else self.rack_price_3p - (self.rack_price_3p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_2p_child = self.overridden_net_price_2p_child if self.overridden_net_price_2p_child is not None else self.rack_price_2p_child - (self.rack_price_2p_child * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_4p = self.overridden_net_price_4p if self.overridden_net_price_4p is not None else self.rack_price_4p - (self.rack_price_4p * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_3p_child = self.overridden_net_price_3p_child if self.overridden_net_price_3p_child is not None else self.rack_price_3p_child - (self.rack_price_3p_child * tac_percentage * default_commission_percentage / 10000)
        self.rate_for_customer_4p_child = self.overridden_net_price_4p_child if self.overridden_net_price_4p_child is not None else self.rack_price_4p_child - (self.rack_price_4p_child * tac_percentage * default_commission_percentage / 10000)

        self.save()

# And if, they w

 
# This next method is for the possibility in the UI that an agent is offered the hotels rack rates and can copy them down into its own system. It takes in the hotel_room_Id and the owner_agent_id        
    @classmethod
    def copy_rack_rates_from_owner(cls, hotel_room_id, agent_id, owner_agent_id):
            owner_room_price = cls.objects.filter(hotel_room_id=hotel_room_id, agent_id=owner_agent_id).first()
            if not owner_room_price:
                raise ValueError("No room price set by the hotel owner for this room.")

            agent_room_price, created = cls.objects.get_or_create(hotel_room_id=hotel_room_id, agent_id=agent_id)

            agent_room_price.rack_price_1p = owner_room_price.rack_price_1p
            agent_room_price.rack_price_2p = owner_room_price.rack_price_2p
            agent_room_price.rack_price_3p = owner_room_price.rack_price_3p
            agent_room_price.rack_price_2p_child = owner_room_price.rack_price_2p_child
            agent_room_price.rack_price_4p = owner_room_price.rack_price_4p
            agent_room_price.rack_price_3p_child = owner_room_price.rack_price_3p_child
            agent_room_price.rack_price_4p_child = owner_room_price.rack_price_4p_child

            agent_room_price.save()

    def __str__(self):
        return f"{self.hotel_room.name} - {self.meal_plan}"

# These activities are just for the hotel listing, where it will say onsite activities and local activities. No need for costing just yet, 
class HotelActivities(models.Model):
        name = models.CharField(max_length=50)
        description = models.CharField(max_length=200)

        customized_hotel = models.ForeignKey(CustomizedHotel, on_delete=models.CASCADE, related_name='hotel_activities')
        onsite_activity = models.BooleanField(default=False)  # If false, then it becomes a Local Activiry
        onsite_activity = models.BooleanField(default=False)
        free_activity = models.BooleanField(default=False)
        can_be_personalised = models.BooleanField(default=False)
        

        def save(self, *args, **kwargs):
            if self.customized_hotel:
                activities_count = HotelActivities.objects.filter(customized_hotel=self.customized_hotel, is_active=True).count()
                if activities_count >= 15:
                    raise ValidationError("Cannot add more than 15 active activities per hotel.")

            super(HotelActivities, self).save(*args, **kwargs)

        
        
class HotelAmenities(models.Model):
        name = models.CharField(max_length=40)
#  We can then have a separation between Hotel Amenities and for each specific room
        customized_hotel = models.ForeignKey(CustomizedHotel, on_delete=models.CASCADE, related_name='hotel_amenities')
        hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
        onsite_activity = models.BooleanField(default=False)
        free_activity = models.BooleanField(default=False)

        def save(self, *args, **kwargs):
            if self.customized_hotel:
                amenities_count = HotelAmenities.objects.filter(customized_hotel=self.customized_hotel, is_active=True).count()
                if amenities_count >= 20:
                    raise ValidationError("Cannot add more than 20 active amenities per hotel.")

            super(HotelAmenities, self).save(*args, **kwargs)
            
class HotelInfo(models.Model):
    customized_hotel = models.ForeignKey(CustomizedHotel, on_delete=models.CASCADE, related_name='hotel_info')
    check_in_time = models.TimeField(help_text="Check-in time")
    check_out_time = models.TimeField(help_text="Check-out time")
    zero_refund_days = models.IntegerField(default=0, blank=True, null=True)
    quarter_refund_days = models.IntegerField(default=0, blank=True, null=True)
    half_refund_days = models.IntegerField(default=0, blank=True, null=True)
    percentage_deposit = models.DecimalField(default=0, decimal_places=2, null=True, blank=True, max_digits=5)

    def clean(self):
        # Validate check-in time
        if self.check_in_time.minute not in [0, 30]:
            raise ValidationError(_('Check-in time must be on the hour or half past the hour.'))

        # Validate check-out time
        if self.check_out_time.minute not in [0, 30]:
            raise ValidationError(_('Check-out time must be on the hour or half past the hour.'))

        if self.zero_refund_days < 0 or self.quarter_refund_days < 0 or self.half_refund_days < 0:
            raise ValidationError(_("Refund days must be positive."))

        if self.percentage_deposit < 0 or self.percentage_deposit > 100:
            raise ValidationError(_("Percentage deposit must be between 0 and 100."))

        super(HotelInfo, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(HotelInfo, self).save(*args, **kwargs)


# @register(Hotel)
# class HotelTranslationOptions(TranslationOptions):
#     fields = ('name', 'description')


# For the frontend logic for the translation:Frontend (React)
# Language Switching:

# Implement a language switcher on your website that allows the user to select their preferred language.
# Store the user's language preference in the state, local storage, or cookies.
# Fetching and Displaying Translated Content:

# When fetching data from your backend, ensure that you retrieve the content based on the user's selected language.
# Your API could either return all language versions of a field (e.g., name_en, name_fr) or just the version for the currently selected language, based on a parameter in the request.
# Fallback Mechanism:

# It's good practice to have a fallback language (usually English) in case the translation for the selected language is not available.
# Implementation Steps
# Install and Setup Translation Library:

# Install django-modeltranslation via pip and configure it in your Django project as per the documentation.
# Create Translations for Models:

# Define which fields you want to be translatable in each model and create the necessary translation options.
# Update Django Admin:

# If you're using Django Admin, update it to work with your translated fields.
# Update your API:

# Adjust your API to handle and deliver translated content based on the user's language preference.
# Frontend Language Selector:

# Implement a language selector on the frontend and manage state accordingly.
# Update Frontend Fetch Logic:

# Modify how your frontend application fetches and displays data to handle the different language versions.