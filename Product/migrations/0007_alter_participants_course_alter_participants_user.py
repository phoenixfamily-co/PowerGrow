# Generated by Django 4.2.4 on 2023-10-01 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0006_alter_participants_course_alter_participants_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participants',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='Product.course'),
        ),
        migrations.AlterField(
            model_name='participants',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
