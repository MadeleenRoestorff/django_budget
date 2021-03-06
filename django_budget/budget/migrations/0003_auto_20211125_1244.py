# Generated by Django 3.2.8 on 2021-11-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_fuellog_advertised_price_per_liters'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuellog',
            name='odometer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fuellog',
            name='station',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='fuellog',
            name='tank_distance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
