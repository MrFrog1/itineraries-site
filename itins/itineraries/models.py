from django.db import models
from region.models import Region
from django.conf import settings
from contacts.models import Contact
from components.models import Component
from django.core.exceptions import ValidationError
from db_changes.models import DbChange
from common.models import Tag


# On this page, and on the components page, we have a problem with pricing. . For example, some things pricing is wildly difficult for 1-3 pax, than it is for 4-7 pax. 
# Some activities, or some itinearies, would only be able to give live prices for pax under 4 or 5. If its a hotel, then the pricing depends on which hotel rooms they take, 
# but we can create a function that assigns them according to some logic. Similarly, with taxis, if there are more than 5 people, then maybe they need 2 taxis, so there would need to be logic there too. 


# One option is that we create a PricingMatrix model, which has Component, ItineraryDay etc as a ForeignKey and then can have a fixed price option (ie, no matter how many guests), pricing per pax (multiplier)
# or range pricing (1-3 this much per pax, or 4-7 this much per pax). Then, we can have a function that calculates the price based on the PricingMatrix.

# Another option is that we have enhanced models for each of the components, and then we can have a function that calculates the price based on the enhanced model.



class Itinerary(models.Model):
    name = models.CharField(max_length=45)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_related")
    expert = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_experts")
    guide = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    verified_by_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Makes Itinerary an abstract base class

    def __str__(self):
        return self.name
    
    
class NonCustomerParticipant(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

   


class AgentItinerary(Itinerary):

    TYPE_CHOICES = [
        ('hiking', 'Hiking'),
        ('fishing', 'Fishing'),
        ('cultural', 'Cultural'),
        ('cuisine', 'Cuisine'), 
    ]
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="agent_itineraries")
    customisable = models.BooleanField(default=False)
    cost_for_1_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_for_2_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_for_3_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_for_4_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    with_leader_cost_for_1_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    with_leader_cost_for_2_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    with_leader_cost_for_3_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    with_leader_cost_for_4_pax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    short_visible_description = models.TextField(max_length=255, blank=True, null=True)
    visible_description = models.TextField(max_length=800, blank=True, null=True)
    price_breakdown = models.BooleanField(default=False)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)


# ratings by month of best time to go 
    
    january_rating = models.IntegerField(default=0)
    february_rating = models.IntegerField(default=0)
    march_rating = models.IntegerField(default=0)
    april_rating = models.IntegerField(default=0)
    may_rating = models.IntegerField(default=0)
    june_rating = models.IntegerField(default=0)
    july_rating = models.IntegerField(default=0)
    august_rating = models.IntegerField(default=0)
    september_rating = models.IntegerField(default=0)
    october_rating = models.IntegerField(default=0)
    november_rating = models.IntegerField(default=0)
    december_rating = models.IntegerField(default=0)

    # Fields for Fixed Group Itinerary
    fixed_group = models.BooleanField(default=False, help_text="Is this a fixed group itinerary?")
    group_start_date = models.DateField(null=True, blank=True, help_text="Start date for the group itinerary.")
    min_group_size = models.IntegerField(null=True, blank=True, help_text="Minimum number of guests for the group.")
    max_group_size = models.IntegerField(null=True, blank=True, help_text="Maximum number of guests for the group.")

    # Relationship with customers and non-customers
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="joined_group_itineraries")
    non_customer_participants = models.ManyToManyField(NonCustomerParticipant, blank=True)


# converts an Agent Itinerary into a Customer itinerary 
    


    def add_non_customer_participant(self, name, phone_number=None, email=None):
        """
        Adds a non-customer participant to the itinerary.
        """
        participant, created = NonCustomerParticipant.objects.get_or_create(
            name=name,
            defaults={'phone_number': phone_number, 'email': email}
        )
        self.non_customer_participants.add(participant)

    def can_be_converted_to_customer_itinerary(self):
        """
        Checks whether the itinerary can be converted to a CustomerItinerary.
        """
        return not self.fixed_group

    def create_customer_itinerary(self, customer):

        if not self.customisable:
            raise ValidationError("This itinerary cannot be customized.")

        if not self.can_be_converted_to_customer_itinerary():
           raise ValidationError(_("This itinerary cannot be converted to a CustomerItinerary."))
    
        
        customer_itinerary = CustomerItinerary.objects.create(
            original_agent_itinerary=self,
            customer=customer,
            region=self.region,
            agent=self.agent,
            expert=self.expert,
            guide=self.guide
        )
        return customer_itinerary
    
class CustomerItinerary(Itinerary):
    original_itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_notes = models.TextField(max_length=800, blank=True, null=True)
    number_of_adults = models.IntegerField()
    number_of_children_6_to_12 = models.IntegerField()
    number_of_infants_0_to_5 = models.IntegerField(default=0)
    number_of_taxis = models.IntegerField()
    number_of_rooms = models.IntegerField()
    agent_listed_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    confirmed = models.BooleanField(default=False)


    # Logic to calculate the limit for number_of_taxis based on the number of people...

    def calculate_default_taxis(self):
        total_people = self.number_of_adults + self.number_of_children_6_to_12 + self.number_of_infants_0_to_5

        # If there's a guide, one spot in a taxi is occupied by the guide
        spots_per_taxi = 4 if self.guide else 5

        # Calculate the number of taxis needed
        taxis_needed = -(-total_people // spots_per_taxi)  # Ceiling division
        return taxis_needed

# If they try to save down and there's no number of taxis, then calculate the number of taxis based on the number of people. Also, if they try to enter too few taxis, then calculate the number of taxis based on the number of people.
    def save(self, *args, **kwargs):
        if not self.number_of_taxis or self.number_of_taxis < self.calculate_default_taxis():
            self.number_of_taxis = self.calculate_default_taxis()
        super(CustomerItinerary, self).save(*args, **kwargs)

class RoomSpecification(models.Model):
    customer_itinerary = models.ForeignKey(CustomerItinerary, related_name='room_specifications', on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    adults_in_room = models.IntegerField(default=2)
    children_in_room = models.IntegerField(default=0)
    infants_in_room = models.IntegerField(default=0)


    # Add validation to ensure the total number of adults and children in rooms 
    # does not exceed the total number of adults and children in the CustomerItinerary
    def clean(self):
        if self.customer_itinerary:
            total_people = self.adults_in_room + self.children_in_room + self.infants_in_room
            max_people = self.customer_itinerary.number_of_adults + self.customer_itinerary.number_of_children_6_to_12 + self.customer_itinerary.number_of_infants_0_to_5
            
            if total_people > max_people:
                raise ValidationError("The number of people in a room exceeds the total number in the CustomerItinerary.")

    def save(self, *args, **kwargs):
        self.clean()
        super(RoomSpecification, self).save(*args, **kwargs)


class ItineraryGroup(models.Model):
    name = models.CharField(max_length=30)
    mandatory_guide = models.BooleanField(default=False)
    mandatory_position_in_itinerary = models.IntegerField(default=0)
    guide = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    override_cost_for_1_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_2_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_3_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_4_pax = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=350)

    def __str__(self):
        return self.name
    

    
class ItineraryGrouping(models.Model):
    customer_itinerary = models.ForeignKey(CustomerItinerary, on_delete=models.CASCADE)
    agent_itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)

    group = models.ForeignKey(ItineraryGroup, on_delete=models.CASCADE)
    visible_guide = models.BooleanField(default=False)
    random_guide = models.BooleanField(default=False)
    guide_price_override = models.IntegerField(blank=True, null=True)
    mandatory_position_in_itinerary = models.IntegerField(default=0)
    override_cost_for_1_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_2_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_3_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_4_pax = models.IntegerField(blank=True, null=True)

    price_visible = models.BooleanField(default=True)
# The net price will never be visible but the price_visible will determine whether the customer can see the pricing, and that will be organised in the front end logic

    override_cost_for_4_pax = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('customer_itinerary', 'group')
        unique_together = ('agent_itinerary', 'group')
    
class ItineraryDay(models.Model):
    name = models.CharField(max_length=30)
    mandatory_guide = models.BooleanField(default=False)
    guide = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    override_cost_for_1_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_2_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_3_pax = models.IntegerField(blank=True, null=True)
    override_cost_for_4_pax = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50)
    itinerary_group = models.ForeignKey(ItineraryGroup, on_delete=models.CASCADE)


    price_visible = models.BooleanField(default=True)
# The net price will never be visible but the price_visible will determine whether the customer can see the pricing, and that will be organised in the front end logic


    def __str__(self):
        return self.name
    
    def calculate_totals(self):
        total_net_price = 0
        total_customer_price = 0
        total_commission = 0

        components = self.itinerarydaycomponent_set.all()
        for component in components:
            # Assuming component.net_price and component.price are calculated and saved
            net_price = component.net_price or 0
            customer_price = component.price or 0

            total_net_price += net_price
            total_customer_price += customer_price
            total_commission += customer_price - net_price

        return {
            'total_net_price': total_net_price,
            'total_customer_price': total_customer_price,
            'total_commission': total_commission
        }


CATEGORY_CHOICES_2 = [
    ('booked', 'Booked'),
    ('contacted', 'Contacted'),
    ('not contacted', 'Not Contacted')
]



class ItineraryDayComponent(models.Model):
    itinerary_day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE)
    # A component can have a contact woh is generally responsible. But here, this contact is the driver, the specific guide they go for, so they can measure how much business they give that driver, that guide etc
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    # So, the copmonent belongs to an agent. But, whhen paired with an itinerary day, then a customer has control of that. We can access all components for an itinerary day of a customer through here
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    customer_note = models.TextField()

    # Additional fields can be added here if needed, such as quantity, notes, etc.

    price_visible = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
# The net price will never be visible but the price_visible will determine whether the customer can see the pricing, and that will be organised in the front end logic

    net_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    customer_price_markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

# The Agent should be able to mark each component as booked, so they can check on the status of their itinerary. In the frontend, they should be able to just click it. or drag itn 
    booking_status = models.CharField(max_length=100, choices=CATEGORY_CHOICES_2, default='not contacted')
    flagged = models.BooleanField(default=False)





# When calling this save, we need to explicitly name the user. Something like instance.save(user=request.user)


    def save(self, *args, **kwargs):
        # Extract user from kwargs if provided
        user = kwargs.pop('user', None)
        
        # Calculate prices before saving
        customer_itinerary = self.itinerary_day.itinerary_group.customer_itinerary
        number_of_people = customer_itinerary.number_of_adults + customer_itinerary.number_of_children_6_to_12 + customer_itinerary.number_of_infants_0_to_5

        # Calculate and set prices
        self.price = self._calculate_price(number_of_people)
        self.net_price = self._calculate_net_price(number_of_people)

        super().save(*args, **kwargs)
        action = "created" if self._state.adding else "updated"
        DbChange.objects.create(
            user=user, 
            description=f"{action} {self}",
            changed_model='ItineraryDayComponent'  # Pass the model name here
        )


        
    def calculate_price(self, number_of_people):
        # If the component has a fixed overall price, use that
        if self.component.fixed_price_overall is not None:
            return self.component.fixed_price_overall
        # If it has a fixed price per person, multiply by the number of people
        elif self.component.fixed_price_per_person is not None:
            return self.component.fixed_price_per_person * number_of_people
        # Otherwise, use the price based on the number of people, if available
        else:
            price_field = f'price_for_{number_of_people}_pax'
            price_per_pax = getattr(self.component, price_field, None)
            return price_per_pax if price_per_pax is not None else 0


    def calculate_net_price(self, number_of_people):
        # Similar logic for net prices
        if self.component.net_fixed_price_overall is not None:
            return self.component.net_fixed_price_overall
        elif self.component.net_fixed_price_per_person is not None:
            return self.component.net_fixed_price_per_person * number_of_people
        else:
            price_field = f'net_price_for_{number_of_people}_pax'
            net_price_per_pax = getattr(self.component, price_field, None)
            return net_price_per_pax if net_price_per_pax is not None else 0



    def _calc_price_from_net(self):
        # Calculate customer price based on net price and markup percentage
        if self.net_price is not None and self.customer_price_markup_percentage is not None:
            markup_multiplier = 1 + (self.customer_price_markup_percentage / 100)
            return self.net_price * markup_multiplier
        return None
    
    # ... any other methods ...


# The UI should have a discount field
