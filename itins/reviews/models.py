# reviews/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from hotels.models import Hotel
from contacts.models import Contact

review_status = [("pending", "Pending"), ("rejected", "Rejected"), ("approved", "Approved")]

class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_customer')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_agent')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    review_description = models.CharField(max_length=220)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    month_of_experience = models.IntegerField(default=0)
    anonymous_review = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=review_status, default="pending")
    visible_to_all = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)
    unhelpful_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)

    def calculate_weight(self):
        return self.unhelpful_count * 1.2 + self.helpful_count + self.click_count * 0.05

    def __str__(self):
        return f"Review by {self.customer} - {self.rating}/5"

class ExternalReviewSource(models.Model):
    name = models.CharField(max_length=50)
    weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.name

class ExternalReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='external_reviews')
    source = models.ForeignKey(ExternalReviewSource, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_count = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.name} review for {self.hotel.name}"