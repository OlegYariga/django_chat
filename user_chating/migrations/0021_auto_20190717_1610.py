# Generated by Django 2.2.1 on 2019-07-17 13:10

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_chating', '0020_auto_20190716_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='url',
            field=models.CharField(default=uuid.UUID('a2efaf01-53a4-4967-a537-365a5c131518'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='identifier',
            field=models.CharField(default=uuid.UUID('d3c74873-c8db-44b2-b475-b94991d64687'), max_length=100),
        ),
        migrations.AlterField(
            model_name='messages',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 17, 13, 10, 7, 835838)),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 17, 13, 10, 7, 815838)),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default=uuid.UUID('c5c853cd-5772-4905-94e2-288747f95645'), max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 17, 13, 10, 7, 815838)),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='token',
            field=models.CharField(default=uuid.UUID('01767acd-1675-45f2-ab4a-60cbc9caa089'), max_length=100),
        ),
        migrations.AlterField(
            model_name='usersauth',
            name='when_online',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 17, 13, 10, 7, 815838)),
        ),
        migrations.CreateModel(
            name='DeletedMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('senddate', models.DateTimeField(default=datetime.datetime(2019, 7, 17, 13, 10, 7, 835838))),
                ('identifier', models.CharField(default=uuid.UUID('e2ad5784-6d61-4ca0-b9fb-43a434de7203'), max_length=100)),
                ('chats', models.ManyToManyField(to='user_chating.Chats')),
            ],
        ),
    ]