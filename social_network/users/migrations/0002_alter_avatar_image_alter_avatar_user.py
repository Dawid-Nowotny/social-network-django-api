# Generated by Django 5.0.6 on 2024-06-04 07:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.ImageField(upload_to='images/avatars'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to=settings.AUTH_USER_MODEL),
        ),
    ]
