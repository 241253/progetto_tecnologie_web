from django import forms
from booking_management.models import Booking


class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('data_ora', 'formatore')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(BookingCreationForm, self).__init__(*args, **kwargs)
        self.fields['formatore'].required = False

    def save(self, commit=True):
        booking = super(BookingCreationForm, self).save(commit=False)
        booking.user_id = self.current_user.id
        if commit:
            booking.save()
        return booking