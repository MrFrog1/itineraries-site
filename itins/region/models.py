from django.db import models
from django.core.exceptions import ValidationError


class Region(models.Model):
    description = models.CharField(max_length=350)
    # Temperature fields
    january_min_temperature = models.IntegerField(default=0)
    february_min_temperature = models.IntegerField(default=0)
    march_min_temperature = models.IntegerField(default=0)
    april_min_temperature = models.IntegerField(default=0)
    may_min_temperature = models.IntegerField(default=0)
    june_min_temperature = models.IntegerField(default=0)
    july_min_temperature = models.IntegerField(default=0)
    august_min_temperature = models.IntegerField(default=0)
    september_min_temperature = models.IntegerField(default=0)
    october_min_temperature = models.IntegerField(default=0)
    november_min_temperature = models.IntegerField(default=0)
    december_min_temperature = models.IntegerField(default=0)

    january_max_temperature = models.IntegerField(default=0)
    february_max_temperature = models.IntegerField(default=0)
    march_max_temperature = models.IntegerField(default=0)
    april_max_temperature = models.IntegerField(default=0)
    may_max_temperature = models.IntegerField(default=0)
    june_max_temperature = models.IntegerField(default=0)
    july_max_temperature = models.IntegerField(default=0)
    august_max_temperature = models.IntegerField(default=0)
    september_max_temperature = models.IntegerField(default=0)
    october_max_temperature = models.IntegerField(default=0)
    november_max_temperature = models.IntegerField(default=0)
    december_max_temperature = models.IntegerField(default=0)
    # Weather fields
    WEATHER_CHOICES = [
        ('sunny', 'Sunny'),
        ('sunny_and_cloudy', 'Sunny and Cloudy'),
        ('cloudy', 'Cloudy'),
        ('light_rain', 'Light Rain'),
        ('monsoon_rain', 'Monsoon Rain'),
        ('snow', 'Snow'),
        # ... (add any other weather types here)
    ]

    january_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    february_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    march_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    april_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    may_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    june_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    july_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    august_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    september_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    october_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    november_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    december_weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)

    def clean(self):
        # Validate temperature ranges
        temperature_fields = [(getattr(self, f'january_min_temperature'), getattr(self, f'january_max_temperature')) for month in range(1, 13)]
        for min_temp, max_temp in temperature_fields:
            if not (-40 <= min_temp <= 50):
                raise ValidationError("Minimum temperature must be between -40 and 50 degrees.")
            if not (-40 <= max_temp <= 50):
                raise ValidationError("Maximum temperature must be between -40 and 50 degrees.")
            if min_temp > max_temp:
                raise ValidationError("Minimum temperature cannot be higher than maximum temperature.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # ... rest of your model ...

    def __str__(self):
        return self.description