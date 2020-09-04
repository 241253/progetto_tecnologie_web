import datetime as dt

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.forms import HiddenInput
from django.http import HttpResponse

from booking_management.models import Booking, BookingStatus


#BOOKING
from user_management.models import Profile


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
        if data < booking_date:
            print('bboking: ', booking_date)
            print('current: ', data)
            raise ValidationError(f"puoi prenotare a partire dal {booking_date.strftime('%d/%m/%Y')}")
        return data

    def save(self, commit=True):
        booking = super(BookingCreationForm, self).save(commit=False)
        profile = Profile.objects.get(user_id=self.current_user.id)
        if profile.saldo >= 20:
            profile.saldo -= 20
            profile.save()
        else:
            return None
        booking.user = self.current_user
        if commit:
            booking.save()
        return booking

#BOOKING_STATUS
class BookingStatusConfirmForm(forms.ModelForm):

    FORMATORI = [(f.id, f.username) for f in User.objects.filter(is_staff=True)]
    formatore= forms.CharField(label='Formatore a cui asseganre la lezione live:', widget=forms.Select(choices=FORMATORI))

    class Meta:
        model = BookingStatus
        fields = ('formatore',)

    def __init__(self, *args, **kwargs):
        self.booking_id = kwargs.pop('booking_id')
        super(BookingStatusConfirmForm, self).__init__(*args, **kwargs)

    def clean_formatore(self):
        formatore_id = self.data['formatore']
        formatore = User.objects.get(id=formatore_id)
        if formatore is None:
            raise forms.ValidationError("Formatore non valido!")
        else:
            return formatore

    def save(self, commit=True):
        booking_status = super(BookingStatusConfirmForm, self).save(commit=False)
        data = self.cleaned_data

        booking_status.stato = '1'
        booking_status.formatore = data['formatore']
        booking_status.booking = Booking.objects.get(id=self.booking_id)

        subject = 'Conferma prenotazione'
        prenotazione = Booking.objects.get(id=self.booking_id)
        utente = User.objects.get(id=prenotazione.user.id)
        message = 'Gentile ' + utente.username + \
                  ',\n\nla prenotazione da lei effettuata in data ' + prenotazione.data.strftime('%d/%m/%Y') + ' alle ore ' + prenotazione.ora.strftime('%H:%M') + ' è stata Confermata.\n' \
                  'Per qualsiasi informazione o necessità visita la sezione contatti del nostro sito www.virgiliancodeonline.it.'
        try:
            send_mail(subject, message, 'virgiliancodeonline@gmail.com', [utente.email], fail_silently=False,)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        if commit:
            booking_status.save()
        return booking_status

class BookingStatusUndoForm(forms.ModelForm):

    FORMATORI = [(f.id, f.username) for f in User.objects.filter(is_superuser=True)]
    formatore= forms.CharField(label='Formatore a cui asseganre la lezione live:', widget=forms.Select(choices=FORMATORI))

    class Meta:
        model = BookingStatus
        fields = ('formatore',)

    def __init__(self, *args, **kwargs):
        self.booking_id = kwargs.pop('booking_id')
        self.user = kwargs.pop('user')
        super(BookingStatusUndoForm, self).__init__(*args, **kwargs)

    def clean_formatore(self):
        formatore_id = self.data['formatore']
        formatore = User.objects.get(id=formatore_id)
        if formatore is None:
            raise forms.ValidationError("Formatore non valido!")
        else:
            return formatore

    def save(self, commit=True):
        booking_status = super(BookingStatusUndoForm, self).save(commit=False)
        data = self.cleaned_data

        booking_status.stato = '0'
        booking_status.formatore = data['formatore']
        booking_status.booking = Booking.objects.get(id=self.booking_id)

        subject = 'Annullamento prenotazione'
        prenotazione = Booking.objects.get(id=self.booking_id)
        utente = User.objects.get(id=prenotazione.user.id)
        message = 'Gentile ' + utente.username + ',\n\nla prenotazione da lei effettuata in data ' + prenotazione.data.strftime('%d/%m/%Y') + \
                  ' alle ore ' + prenotazione.ora.strftime('%H:%M') + \
                  'è stata annullata in quanto non abbiamo formatori disponibile per quel giorno.\n' \
                  'Lo staff di virgiliancode si scusa per l\'inconveniente e la invitiamo ad effettuare una nuova prenotazione ad un orario differente.\n\n' \
                  'Per qualsiasi informazione o necessità visita la sezione contatti del nostro sito www.virgiliancodeonline.it.'
        try:
            send_mail(subject, message, 'virgiliancodeonline@gmail.com', [utente.email], fail_silently=False,)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        if commit:
            booking_status.save()
        return booking_status