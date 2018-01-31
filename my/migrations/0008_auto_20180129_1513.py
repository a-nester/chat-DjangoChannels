# Generated by Django 2.0.1 on 2018-01-29 15:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my', '0007_auto_20180129_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='users',
        ),
        migrations.AddField(
            model_name='rooms',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]