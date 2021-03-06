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
    path('check_online/<url>', views.check_online, name='check_online'),
    path('edit_userinfo', views.edit_userinfo, name='edit_userinfo'),
    path('open_access_to_chat/<url>', views.open_access_to_chat, name='open_access_to_chat'),
    path('get_access_to_chat/<url>', views.get_access_to_chat, name='get_access_to_chat'),
    path('delete_message/', views.delete_message, name='delete_message'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('get_delete_message/', views.get_delete_message, name='get_delete_message'),
    path('help/', views.help, name='help'),
    path('check_new_messages/', views.check_new_messages, name='check_new_messages'),
    path('additional/', views.additional, name='additional'),
    path('lk/get_aes_key/<url>', views.get_aes_key, name='get_aes_key'),

]
