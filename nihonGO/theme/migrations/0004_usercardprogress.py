# Generated by Django 5.1.1 on 2024-10-29 17:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0003_deck_description_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCardProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_reviewed', models.DateTimeField(default=django.utils.timezone.now)),
                ('next_review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ease_factor', models.FloatField(default=2.5)),
                ('interval', models.IntegerField(default=1)),
                ('repetition_count', models.IntegerField(default=0)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theme.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
