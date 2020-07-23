from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    #LOGIN URL
    path('login/', auth_views.LoginView.as_view(), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #REGISTARTION URL
    path('registration/', views.create_user, name='registration'),
    #USER URL
    path('user/<int:pk>/', views.UserPage.as_view(), name='user_page'),
    path('user/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('user/update/complete/', views.UserUpdateComplete, name='user_update_complete'),
    #STAFF URL
    path('redirect/', views.login_redirect, name='login_redirect_url'),
    path('staff/home/', views.StaffPage.as_view(), name='staff_page'),
]
