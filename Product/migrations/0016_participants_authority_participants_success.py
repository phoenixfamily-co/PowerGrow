# Generated by Django 4.2.4 on 2023-12-18 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0015_alter_sessions_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='participants',
            name='authority',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='participants',
            name='success',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]