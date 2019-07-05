# Generated by Django 2.2.1 on 2019-07-05 20:02

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0005_auto_20190705_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('74020e36-0efe-4794-a38b-17258db72798'), max_length=100),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 5, 23, 2, 30, 256241)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('fde44b59-3d45-4925-a4eb-d8b0f28e5daa'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('60efae1e-4586-45a0-975a-6bd32cb4e604'), max_length=100),
        ),
    ]