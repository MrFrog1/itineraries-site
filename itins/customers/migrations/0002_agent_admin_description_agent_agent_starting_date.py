# Generated by Django 4.2.9 on 2024-01-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='admin_description',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='agent_starting_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]