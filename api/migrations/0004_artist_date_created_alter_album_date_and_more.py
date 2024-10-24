# Generated by Django 5.0.6 on 2024-10-20 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_ethnicity_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='date_created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='slug',
            field=models.SlugField(auto_created=True, null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='slug',
            field=models.SlugField(auto_created=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(auto_created=True, null=True, unique=True),
        ),
    ]
