# Generated by Django 2.2.1 on 2019-07-07 11:00

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0007_auto_20190707_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('3b707072-711a-4af2-9f07-2c7c35205fe0'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='chats',
            field=models.ManyToManyField(to='user_chating.Chats'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='identifier',
            field=models.CharField(default=uuid.UUID('3128105e-c0f0-4a9f-8a77-a022c24b0838'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 7, 14, 0, 45, 351831)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 7, 14, 0, 45, 348831)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('56521e66-f77f-4692-a46b-7abcfd70029f'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('4d7f63a4-370a-48f8-8e81-5d023344751c'), max_length=100),
        ),
    ]
