from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from booking_management.forms import BookingCreationForm
from booking_management.models import Booking


class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingCreationForm
    template_name = 'booking_management/create_booking.html'
    success_url = reverse_lazy('booking_success')

    def get_form_kwargs(self):
        kwargs = super(CreateBookingView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class BookingSuccessView(TemplateView):
    template_name = 'booking_management/success_booking.html'

class BookingAdminView(TemplateView):
    template_name = 'booking_management/booking_admin.html'

class BookingStaffView(TemplateView):
    template_name = 'booking_management/booking_staff.html'