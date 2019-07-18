from django.db import models
from datetime import datetime
from uuid import uuid4
from django.contrib.auth.models import User


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid4())
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50, default=None)
    last_login = models.DateTimeField(default=datetime.utcnow())
    is_online = models.BooleanField(default=False)
    when_online = models.DateTimeField(default=datetime.utcnow())

    def create(self):
        self.save()

    def delete(self):
        self.delete()


class UsersAuth(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100, default=uuid4())
    is_online = models.BooleanField(default=False)
    when_online = models.DateTimeField(default=datetime.utcnow())


def is_authorized(token):
    user_auth = UsersAuth.objects.filter(token=token).exists()
    if user_auth:
        return True
    return False


class Chats(models.Model):
    users = models.ManyToManyField(Users)
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=100, default=uuid4())
    is_opened = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Messages(models.Model):
    chats = models.ManyToManyField(Chats)
    username = models.CharField(max_length=50)
    message = models.TextField()
    senddate = models.DateTimeField(default=datetime.utcnow())
    identifier = models.CharField(max_length=100, default=uuid4())


class DeletedMessages(models.Model):
    chats = models.ManyToManyField(Chats)
    username = models.CharField(max_length=50)
    message = models.TextField()
    senddate = models.DateTimeField(default=datetime.utcnow())
    identifier = models.CharField(max_length=100, default=uuid4())