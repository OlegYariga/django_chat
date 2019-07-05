# Generated by Django 2.2.1 on 2019-07-04 13:04

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0003_auto_20190704_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 16, 4, 38, 940154)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('55e90f08-e0f4-409d-b8e0-51648637661a'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('9adb453a-4c08-4bc4-95fc-54348a3f4e01'), max_length=100),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
