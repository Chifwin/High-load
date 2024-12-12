# Generated by Django 5.1.1 on 2024-10-21 18:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user'], name='user_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='status_idx'),
        ),
    ]