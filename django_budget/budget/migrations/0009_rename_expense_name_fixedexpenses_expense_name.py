# Generated by Django 3.2.8 on 2021-12-01 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_delete_necessities'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixedexpenses',
            old_name='expense_name',
            new_name='Expense_name',
        ),
    ]
