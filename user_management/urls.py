from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import path, converters
from . import views
from django.urls.converters import IntConverter, register_converter

urlpatterns = [
    #LOGIN URL
    path('login/', auth_views.LoginView.as_view(), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #REGISTARTION URL
    path('registration/', views.create_user, name='registration'),
    #USER URL
    path('user/<int:pk>/', views.UserPage.as_view(), name='user_page'),
    path('user/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('user/lesson/', views.UserPurchasedLessonView.as_view(), name='user_lesson'),
    path('user/update/complete/', views.UserUpdateComplete, name='user_update_complete'),
    #STAFF URL
    path('redirect/', views.login_redirect, name='login_redirect_url'),
    path('staff/home/', views.StaffPage.as_view(), name='staff_page'),
    path('staff/list/', views.StaffList.as_view(), name='staff_list'),
    path('staff/add/', views.create_staff, name='create_staff'),
    path('staff/remove/<int:pk>', views.DeleteStaff.as_view(), name='delete_staff'),
    path('staff/edit/<int:pk>', views.UpdateStaff.as_view(), name='update_staff'),
    path('staff/detail/<int:pk>', views.DetailStaff.as_view(), name='detail_staff'),
    path('staff/detail/update/<int:pk>', views.StaffDetailUpdate.as_view(), name='detail_update_staff'),
    path('staff/detail/update/complete/', views.StaffDetailUpdateComplete, name='staff_detail_update_complete'),
]
