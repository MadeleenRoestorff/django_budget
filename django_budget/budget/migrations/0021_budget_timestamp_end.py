# Generated by Django 3.2.8 on 2022-01-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0020_auto_20211231_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='timestamp_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]