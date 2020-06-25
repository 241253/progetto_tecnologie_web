from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    #LOGIN URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #REGISTARTION URL
    path('registration/', views.create_user, name='registration'),
    #USER URL
    path('user_profile/', views.create_user, name='user_profile'),
]
