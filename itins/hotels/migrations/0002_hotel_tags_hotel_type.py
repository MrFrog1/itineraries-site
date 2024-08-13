# Generated by Django 5.0.3 on 2024-07-10 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='tags',
            field=models.ManyToManyField(blank=True, to='common.tag'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='type',
            field=models.CharField(choices=[('farmstay', 'Farmstay'), ('heritage', 'Heritage Hotel'), ('beach', 'Beach'), ('jungle', 'Jungle/Wildlife')], default='hi', max_length=20),
            preserve_default=False,
        ),
    ]
