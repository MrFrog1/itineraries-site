# Generated by Django 3.2.24 on 2024-07-26 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_auto_20240725_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='payment_type',
            field=models.CharField(choices=[('paytm', 'PayTM'), ('gpay', 'Gpay'), ('upi', 'UPI'), ('net_transfer', 'Net Transfer'), ('cash', 'Cash'), ('visa', 'Visa'), ('mastercard', 'MasterCard'), ('amex', 'Amex'), ('foreign currency', 'Foreign Currency')], max_length=20, unique=True),
        ),
    ]
