from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    #BOOKING
    path('prenotazioni/', views.CreateBookingView.as_view(), name='booking'),
    path('prenotazioni/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('prenotazioni/success/', views.BookingErrorView.as_view(), name='booking_error'),
    path('prenotazioni/staff/', views.BookingAdminView.as_view(), name='booking_admin'),
    path('prenotazioni/admin/', views.BookingStaffView.as_view(), name='booking_staff'),
    #BOOKING_STATUS
    path('prenotazioni/detail/confirm/<int:booking_id>', views.CreateBookingStatusView.as_view(), name='booking_status_confirm'),
    path('prenotazioni/detail/undo/<int:booking_id>', views.UndoBookingStatusView.as_view(), name='booking_status_undo'),
    #USER_BOOKING
    path('prenotazioni/user/detail', views.UserBookingView.as_view(), name='user_booking'),
]