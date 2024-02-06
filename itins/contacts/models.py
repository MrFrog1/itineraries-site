from django.db import models
from customers.models import Agent
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_contact_email(value):
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError("Invalid email format")


class ContactCategory(models.Model):
    name = models.CharField(max_length=50)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ContactBusiness(models.Model):
    business_name = models.CharField(max_length=100)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50)
    business_website = models.URLField()
    # Other fields ...

    def __str__(self):
        return self.business_name
    
# What additional customisation can we have for a Contact Category or a Contact? There's name etc and pricing component is handled in Components, so maybe fine
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    preferred_first_name = models.CharField(max_length=50)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    daily_rate_where_appropriate = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(ContactCategory)
    business = models.ForeignKey(ContactBusiness, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    whatsapp_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email_address = models.EmailField(validators=[validate_contact_email])


    def __str__(self):
        return self.name
    
    # Other fields ...



