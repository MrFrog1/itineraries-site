# Generated by Django 3.2.24 on 2024-03-05 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('components', '0001_initial'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componenttype',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='component',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='component',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        migrations.AddField(
            model_name='component',
            name='hotel_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotels.hotelroom'),
        ),
    ]
