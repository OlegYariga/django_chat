from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lk/', views.lk, name='lk'),
    path('accounts/login/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('delete_chat/', views.delete_chat, name='delete_chat'),
    path('lk/<url>', views.chatting, name='chatting'),
    path('get_message', views.get_message, name='get_message'),
    path('add_users/<url>', views.add_users, name='add_users'),
]
