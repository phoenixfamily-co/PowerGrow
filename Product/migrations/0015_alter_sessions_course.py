# Generated by Django 4.2.4 on 2023-12-13 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0014_remove_days_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions', to='Product.course'),
        ),
    ]
