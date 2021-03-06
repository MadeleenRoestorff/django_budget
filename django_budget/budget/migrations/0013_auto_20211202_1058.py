# Generated by Django 3.2.8 on 2021-12-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='budget',
            name='timestamp_created_server',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='budget',
            name='timestamp_updated_server',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
