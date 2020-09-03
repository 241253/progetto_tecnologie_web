from django.contrib import admin
from booking_management.models import Booking, BookingStatus

admin.site.register(Booking)
admin.site.register(BookingStatus)