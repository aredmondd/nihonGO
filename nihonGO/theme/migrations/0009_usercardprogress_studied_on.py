# Generated by Django 5.1.1 on 2024-12-02 17:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0008_usercardprogress_correctcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercardprogress',
            name='studied_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
