# Generated by Django 4.2.10 on 2024-08-06 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_potentialagent_useragent_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='potentialagent',
            name='accompanying_agent',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='agent_starting_date',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='converted_user',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='default_commission_percentage',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='default_organisation_fee',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='is_converted',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='join_date',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='sustainability_practices',
        ),
        migrations.RemoveField(
            model_name='potentialagent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_address',
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='potentialagent',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='potentialagent',
            name='admin_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='potentialagent',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='potentialagent',
            name='business_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='potentialagent',
            name='short_bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]