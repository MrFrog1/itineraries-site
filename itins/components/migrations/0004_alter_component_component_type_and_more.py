# Generated by Django 4.2.10 on 2024-08-08 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_alter_contact_categories_and_more'),
        ('components', '0003_component_component_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='component_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.componenttype'),
        ),
        migrations.AlterField(
            model_name='component',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        migrations.AlterField(
            model_name='component',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='fitness_level',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('ironman', 'Ironman'), ('tough', 'Tough'), ('challenging', 'Challenging'), ('moderate', 'Moderate'), ('easy', 'Easy')], default='all', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='wheelchair_accessible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]