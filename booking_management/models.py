from django.contrib.auth.models import User
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_ora = models.DateTimeField(verbose_name='Data e ora ( dd/mm/aaaa hh:mm ):')

    def __str__(self):
        return f'prenotazione di {self.user.username} il giorno {self.data_ora}, #{self.id}'