# Generated by Django 4.2.9 on 2024-01-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0003_itinerarydaycomponent_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentitinerary',
            name='short_visible_description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]