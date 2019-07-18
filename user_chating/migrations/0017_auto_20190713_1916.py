# Generated by Django 2.2.1 on 2019-07-13 16:16

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0016_auto_20190713_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('faa58401-2d2b-40a8-afbd-84468e9035e5'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='identifier',
            field=models.CharField(default=uuid.UUID('c2f7bcbb-6f8a-4406-9daa-7d539b906195'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 19, 16, 1, 179194)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 19, 16, 1, 175193)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('ad9b7ec0-63be-40fd-878e-d8fe26d9e7bf'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 16, 16, 1, 175193)),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('066fa7c1-2b07-4db4-b137-c8b44d6f7386'), max_length=100),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 16, 16, 1, 176193)),
        ),
    ]