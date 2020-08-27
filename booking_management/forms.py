import datetime as dt
from django import forms
from booking_management.models import Booking


class BookingCreationForm(forms.ModelForm):

    class Meta:
        HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(8, 13)] + [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(15, 19)]
        model = Booking
        fields = ('data','ora')
        widgets = {'ora': forms.Select(choices=HOUR_CHOICES)}

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(BookingCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        booking = super(BookingCreationForm, self).save(commit=False)
        booking.user = self.current_user
        if commit:
            booking.save()
        return booking