from uuid import uuid4
from django.contrib import admin
from .models import Users, UsersAuth, Chats, Messages,DeletedMessages
# Register your models here.

admin.site.register(UsersAuth)
admin.site.register(Users)
admin.site.register(Chats)
admin.site.register(Messages)
admin.site.register(DeletedMessages)