# Generated by Django 3.0.6 on 2020-05-06 19:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("circles", "0014_auto_20200506_2128"),
    ]

    operations = [
        migrations.RemoveField(model_name="event", name="participants"),
    ]