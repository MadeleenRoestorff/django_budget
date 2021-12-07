# Generated by Django 3.2.8 on 2021-12-07 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0016_auto_20211206_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='income_in_cents',
            new_name='income_list_in_cents',
        ),
        migrations.AddField(
            model_name='expense',
            name='category_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='remaining_by_category_in_cents',
            field=models.JSONField(blank=True, null=True),
        ),
    ]