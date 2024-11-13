# Generated by Django 4.1 on 2024-11-06 11:04

import accounts.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]
