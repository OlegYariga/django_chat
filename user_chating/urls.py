from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lk/', views.lk, name='lk'),
    path('accounts/login/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('create_chat/', views.create_chat, name='create_chat'),
]
