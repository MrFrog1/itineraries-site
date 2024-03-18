from django.db import models
from django.conf import settings
from hotels.models import Hotel
from contacts.models import Contact

# Create your models here.

review_status = [("pending", "Pending"), ("rejected", "Rejected"), ("approved", "Approved")]

class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name ='reviews_customer')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name ='reviews_agent')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    review_description = models.CharField(max_length=220)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    month_of_experience = models.IntegerField(default=0)
    anonymous_review = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices= review_status, default="pending")

    # Visibility control
    visible_to_all = models.BooleanField(default=True)  # False for agent's private review

    # Counters
    helpful_count = models.PositiveIntegerField(default=0)
    unhelpful_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)

    def calculate_weight(self):
        # Weight calculation based on helpful, unhelpful counts and clicks
        return self.unhelpful_count * 1.2 + self.helpful_count + self.click_count* 0.05

    def __str__(self):
        return f"Review by {self.customer} - {self.rating}/5"
