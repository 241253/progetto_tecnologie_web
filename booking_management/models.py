import datetime as dt
from django.contrib.auth.models import User
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(verbose_name='Data ( gg/mm/aaaa):')
    ora = models.TimeField(default=dt.time(00, 00))

    def __str__(self):
        return f'prenotazione di {self.user.username} il giorno {self.data_ora}, #{self.id}'

class BookingStatus(models.Model):
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE)
    formatore = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    stato = models.CharField(max_length=20, choices=(('A','Annullato'), ('C','Confermato')))