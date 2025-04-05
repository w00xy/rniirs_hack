# Generated by Django 4.1 on 2025-04-05 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='liked',
            field=models.ManyToManyField(related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
