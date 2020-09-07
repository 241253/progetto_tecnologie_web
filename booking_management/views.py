from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, FormView
from booking_management.forms import BookingCreationForm, BookingStatusConfirmForm, BookingStatusUndoForm
from booking_management.models import Booking, BookingStatus
import datetime as dt

#BOOKING

@method_decorator(login_required, name='dispatch')
class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingCreationForm
    template_name = 'booking_management/create_booking.html'
    success_url = reverse_lazy('booking_success')

    def get_form_kwargs(self):
        kwargs = super(CreateBookingView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator(login_required, name='dispatch')
class BookingSuccessView(TemplateView):
    template_name = 'booking_management/success_booking.html'

@method_decorator(login_required, name='dispatch')
class BookingErrorView(TemplateView):
    template_name = 'booking_management/error_booking.html'

@method_decorator(login_required, name='dispatch')
class BookingAdminView(TemplateView):
    template_name = 'booking_management/booking_admin.html'

    def get_context_data(self, **kwargs):
        context = super(BookingAdminView, self).get_context_data(**kwargs)
        booking = [x for x in Booking.objects.all().order_by('data', 'ora') if x not in Booking.objects.filter(id__in=[x.booking.id for x in BookingStatus.objects.all()])]
        booking_detail = BookingStatus.objects.all().order_by('stato')
        context['booking'] = booking
        context['booking_detail'] = booking_detail
        return context

@method_decorator(login_required, name='dispatch')
class BookingStaffView(TemplateView):
    template_name = 'booking_management/booking_staff.html'

    def get_context_data(self, **kwargs):
        context = super(BookingStaffView, self).get_context_data(**kwargs)
        context['booking'] = BookingStatus.objects.filter(formatore=self.request.user, stato='1', booking__data__gte=dt.date.today()).order_by('booking__data', 'booking__ora')
        context['booking_past'] = BookingStatus.objects.filter(formatore=self.request.user, stato='1', booking__data__lt=dt.date.today()).order_by('booking__data', 'booking__ora')
        return context

#BOOKING_STATUS
@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
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
            form.save()
            return super(UndoBookingStatusView, self).form_valid(form)
        else:
            return super(UndoBookingStatusView, self).form_valid(form)

#USER_BOOKING
@method_decorator(login_required, name='dispatch')
class UserBookingView(TemplateView):
    template_name = 'user_management/user/user_booking.html'

    def get_context_data(self, **kwargs):
        context = super(UserBookingView, self).get_context_data(**kwargs)
        context['booking'] = Booking.objects.filter(user_id=self.request.user.id).exclude(id__in=[x.booking.id for x in BookingStatus.objects.filter(booking__user_id=self.request.user.id)])
        context['booking_status'] = BookingStatus.objects.filter(booking__user_id=self.request.user.id, booking__data__gte=dt.date.today()).order_by('-stato', 'booking__data', 'booking__ora')
        context['booking_past'] = BookingStatus.objects.filter(booking__user_id=self.request.user.id, booking__data__lt=dt.date.today()).order_by('-stato', 'booking__data', 'booking__ora')
        return context