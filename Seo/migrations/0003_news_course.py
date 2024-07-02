# Generated by Django 4.2.4 on 2024-07-01 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0021_remove_days_end'),
        ('Seo', '0002_news_date_alter_news_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='Product.course'),
        ),
    ]