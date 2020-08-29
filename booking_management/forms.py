import datetime as dt
from django import forms
from django.core.exceptions import ValidationError

from booking_management.models import Booking, BookingStatus


#BOOKING
class BookingCreationForm(forms.ModelForm):

    class Meta:
        HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(8, 13)] + [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(15, 19)]
        model = Booking
        fields = ('data', 'ora')
        widgets = {'ora': forms.Select(choices=HOUR_CHOICES)}

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(BookingCreationForm, self).__init__(*args, **kwargs)

    def clean_data(self):
        data = self.cleaned_data['data']
        booking_date = (dt.date.today() + dt.timedelta(days=3))
        if data <= booking_date:
            raise ValidationError(f"puoi prenotare a partire dal {booking_date.strftime('%d/%m/%Y')}")
        return data

    def save(self, commit=True):
        booking = super(BookingCreationForm, self).save(commit=False)
        booking.user = self.current_user
        if commit:
            booking.save()
        return booking

#BOOKING_STATUS
class BookingStatusConfirmForm(forms.ModelForm):

    class Meta:
        model = BookingStatus
        fields = ('formatore',)

    def __init__(self, *args, **kwargs):
        self.booking_id = kwargs.pop('booking_id')##########risolvere questo problem o qui o nella save!!!!#############
        super(BookingStatusConfirmForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        booking_status = super(BookingStatusConfirmForm, self).save(commit=False)
        booking_status.booking_id = self.booking_id
        booking_status.stato = '1'
        if commit:
            booking_status.save()
        return booking_status