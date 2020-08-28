from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('prenotazioni/', views.CreateBookingView.as_view(), name='booking'),
    path('prenotazioni/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('prenotazioni/staff/', views.BookingAdminView.as_view(), name='booking_admin'),
    path('prenotazioni/admin/', views.BookingStaffView.as_view(), name='booking_staff'),
]