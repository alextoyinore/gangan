# Generated by Django 5.0.6 on 2024-10-21 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_user_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='title',
            new_name='name',
        ),
    ]
