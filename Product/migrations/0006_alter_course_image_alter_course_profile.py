# Generated by Django 4.2.4 on 2023-09-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_alter_course_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
