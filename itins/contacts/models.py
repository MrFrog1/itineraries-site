from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_contact_email(value):
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError("Invalid email format")


class ContactCategory(models.Model):
    name = models.CharField(max_length=50)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def create_default_categories(cls, agent):
        default_categories = ['Taxis', 'Guides', 'Hotels', 'Restaurants']
        for category in default_categories:
            cls.objects.create(name=category, agent=agent)


class ContactBusiness(models.Model):
    business_name = models.CharField(max_length=100)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    business_website = models.URLField(blank=True, null=True)
    # Other fields ...

    def __str__(self):
        return self.business_name
    
# What additional customisation can we have for a Contact Category or a Contact? There's name etc and pricing component is handled in Components, so maybe fine
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    preferred_first_name = models.CharField(max_length=50, null=True, blank=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_visible_to_others = models.BooleanField(default=False)
    daily_rate_where_appropriate = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    categories = models.ManyToManyField(ContactCategory, blank=True)
    business = models.ForeignKey(ContactBusiness, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(5)], max_digits=5, decimal_places=2, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=50, null=True, blank=True )
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email_address = models.EmailField(validators=[validate_contact_email], null=True, blank=True)


    def __str__(self):
        return self.name
    
    # Other fields ...
