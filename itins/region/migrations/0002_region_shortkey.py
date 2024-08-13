from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='shortkey',
            field=models.CharField(max_length=55, unique=True, null=True),
        ),
    ]