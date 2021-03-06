# Generated by Django 2.2.1 on 2019-07-15 08:56

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0018_auto_20190713_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='is_opened',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('77205cd5-0b8f-42b4-bd55-3bb1bc0b68d7'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='identifier',
            field=models.CharField(default=uuid.UUID('6ea89a83-1bfa-42a6-a4a9-d6729dbd10c8'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 11, 56, 3, 904257)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 11, 56, 3, 884257)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('798d6c12-542f-4ec9-a701-a2bc43e43ae8'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 56, 3, 884257)),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('d8019a56-ccbc-484e-91ae-87978a60514f'), max_length=100),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 56, 3, 884257)),
        ),
    ]
