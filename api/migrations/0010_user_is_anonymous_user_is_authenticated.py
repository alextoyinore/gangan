# Generated by Django 5.0.6 on 2024-10-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_user_city_remove_user_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
