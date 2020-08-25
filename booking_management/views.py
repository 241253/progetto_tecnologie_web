from django.urls import reverse_lazy
from django.views.generic import CreateView
from booking_management.forms import BookingCreationForm
from booking_management.models import Booking


class CreateBooking(CreateView):
    model = Booking
    form_class = BookingCreationForm
    template_name = 'booking_management/create_booking.html'
    success_url = reverse_lazy('homePage')

    def get_form_kwargs(self):
        kwargs = super(CreateBooking, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
