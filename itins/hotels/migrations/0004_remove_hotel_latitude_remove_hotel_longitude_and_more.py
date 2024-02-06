# Generated by Django 4.2.9 on 2024-01-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_customizedhotel_serves_alcohol_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='longitude',
        ),
        migrations.AddField(
            model_name='customizedhotel',
            name='wheelchair_accessible',
            field=models.BooleanField(default=False),
        ),
    ]