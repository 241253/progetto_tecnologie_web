import datetime as dt

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

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
        booking_date = (dt.date.today() + dt.timedelta(days=7))
        if data < booking_date:
            raise ValidationError(f"puoi prenotare a partire dal {booking_date.strftime('%d/%m/%Y')}")
        if data.weekday() == 6 or data.weekday() == 5:
            raise ValidationError('Le prenotazioni non sono disponibili il sabato e la domenica')

        return data

    def save(self, commit=True):
        booking = super(BookingCreationForm, self).save(commit=False)
        booking.user = self.current_user

        subject = 'Prenotazione lezione live'
        message = 'Mail inviata da: ' + booking.user.username + ' ('+ booking.user.email + ')' + "\n\nL'utente " + booking.user.username + \
                   ' vorrebbe effettuare una prenotazione in data: ' + booking.data.strftime('%d/%m/%Y') + ' alle ore ' + booking.ora.strftime('%H:%M') + '.\n\n' + \
                   'Confermare o annullare la prenotazione'

        try:
            send_mail(subject, message, 'virgiliancodeonline@gmail.com', ['virgiliancodeonline@gmail.com'], fail_silently=False, )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

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
        self.fields['formatore'].widget = forms.Select(choices=[(f.id, f.username) for f in User.objects.filter(is_staff=True)])

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
        message = 'Gentile ' + utente.first_name + ',\n\nla prenotazione da lei effettuata in data ' + prenotazione.data.strftime('%d/%m/%Y') + ' alle ore ' + prenotazione.ora.strftime('%H:%M') + ' è stata confermata.\n' + 'Per qualsiasi informazione o necessità visiti la sezione contatti del nostro sito www.virgiliancodeonline.it.'
        try:
            send_mail(subject, message, 'virgiliancodeonline@gmail.com', [utente.email], fail_silently=False,)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        if commit:
            booking_status.save()
        return booking_status

class BookingStatusUndoForm(forms.ModelForm):

    class Meta:
        model = BookingStatus
        exclude = ['booking', 'stato', 'formatore']

    def __init__(self, *args, **kwargs):
        self.booking_id = kwargs.pop('booking_id')
        self.user = kwargs.pop('user')
        super(BookingStatusUndoForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        booking_status = super(BookingStatusUndoForm, self).save(commit=False)
        data = self.cleaned_data

        booking_status.stato = '0'
        booking_status.formatore = User.objects.filter(is_superuser=True)[0]
        booking_status.booking = Booking.objects.get(id=self.booking_id)

        subject = 'Annullamento prenotazione'
        prenotazione = Booking.objects.get(id=self.booking_id)
        utente = User.objects.get(id=prenotazione.user.id)
        message = 'Gentile ' + utente.first_name + ',\n\nla prenotazione da lei effettuata in data ' + prenotazione.data.strftime('%d/%m/%Y') + \
                  ' alle ore ' + prenotazione.ora.strftime('%H:%M') + \
                  ' è stata annullata in quanto non abbiamo formatori disponibili per quel giorno.\n' \
                  'Lo staff di virgiliancode si scusa per l\'inconveniente e la invitiamo ad effettuare una nuova prenotazione ad un giorno o ad un orario differente.\n\n' \
                  'Per qualsiasi informazione o necessità visiti la sezione contatti del nostro sito www.virgiliancodeonline.it.'
        try:
            send_mail(subject, message, 'virgiliancodeonline@gmail.com', [utente.email], fail_silently=False,)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        if commit:
            booking_status.save()
        return booking_status