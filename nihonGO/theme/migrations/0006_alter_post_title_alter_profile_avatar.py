# Generated by Django 5.1.1 on 2024-11-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0005_alter_card_deck_alter_card_english_translation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='profile_images/default.jpg', upload_to='profile_images'),
        ),
    ]