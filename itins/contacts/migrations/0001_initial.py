# Generated by Django 3.2.24 on 2024-03-05 14:35

import contacts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('preferred_first_name', models.CharField(max_length=50)),
                ('daily_rate_where_appropriate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('whatsapp_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254, validators=[contacts.models.validate_contact_email])),
            ],
        ),
        migrations.CreateModel(
            name='ContactBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('gst_number', models.CharField(max_length=50)),
                ('business_website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
