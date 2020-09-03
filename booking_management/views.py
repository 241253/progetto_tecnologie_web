from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView
from booking_management.forms import BookingCreationForm, BookingStatusConfirmForm, BookingStatusUndoForm
from booking_management.models import Booking, BookingStatus

#BOOKING
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

    def get_context_data(self, **kwargs):
        context = super(BookingAdminView, self).get_context_data(**kwargs)
        booking = [x for x in Booking.objects.all().order_by('data', 'ora') if x not in Booking.objects.filter(id__in=[x.booking.id for x in BookingStatus.objects.all()])]
        booking_detail = BookingStatus.objects.all().order_by('stato')
        context['booking'] = booking
        context['booking_detail'] = booking_detail
        return context

class BookingStaffView(TemplateView):
    template_name = 'booking_management/booking_staff.html'

#BOOKING_STATUS
class CreateBookingStatusView(FormView):

    form_class = BookingStatusConfirmForm
    template_name = 'booking_management/confirm_booking.html'
    success_url = reverse_lazy('booking_admin')

    def get_form_kwargs(self):
        kwargs = super(CreateBookingStatusView, self).get_form_kwargs()
        kwargs['booking_id'] = self.kwargs.get('booking_id')
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super(CreateBookingStatusView, self).form_valid(form)

#BOOKING_STATUS
class UndoBookingStatusView(FormView):

    form_class = BookingStatusUndoForm
    template_name = 'booking_management/undo_booking.html'
    success_url = reverse_lazy('booking_admin')

    def get_form_kwargs(self):
        kwargs = super(UndoBookingStatusView, self).get_form_kwargs()
        kwargs['booking_id'] = self.kwargs.get('booking_id')
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            print('giusto')
            form.save()
            return super(UndoBookingStatusView, self).form_valid(form)
        else:
            print('sbagliato')
            return super(UndoBookingStatusView, self).form_valid(form)