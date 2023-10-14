# Generated by Django 4.2.4 on 2023-10-14 12:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_user_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
