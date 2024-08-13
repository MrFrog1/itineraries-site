# Generated by Django 4.2.10 on 2024-08-10 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0004_alter_component_component_type_and_more'),
        ('media', '0004_photo_primary_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='category',
        ),
        migrations.AddField(
            model_name='photo',
            name='component',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='components.component'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['uploader', 'verified_by_admin'], name='media_photo_uploade_a9a2b3_idx'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['region'], name='media_photo_region__d09347_idx'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['hotel'], name='media_photo_hotel_i_7434fb_idx'),
        ),
    ]
