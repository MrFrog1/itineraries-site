# Generated by Django 3.2.24 on 2024-03-05 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_user_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprofile',
            name='location',
        ),
    ]