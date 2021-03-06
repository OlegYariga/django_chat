# Generated by Django 2.2.1 on 2019-07-13 16:13

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0014_auto_20190713_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('245c764c-9a8d-42f2-bef8-905259de3071'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='identifier',
            field=models.CharField(default=uuid.UUID('2599364e-2658-4e50-a870-6f4a58e9ed6a'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 19, 13, 23, 602181)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 19, 13, 23, 598181)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('888da136-d47a-4c4d-9b43-7221974ea9a2'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 16, 13, 23, 598181)),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('d34a663e-3fb1-4f2f-89ba-2197cc3f87eb'), max_length=100),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 16, 13, 23, 599181)),
        ),
    ]
