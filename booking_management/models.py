from django.contrib.auth.models import User
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_ora = models.DateTimeField()
    formatore = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='formatore')

    def __str__(self):
        return f'prenotazione di {self.user.username} il giorno {self.data_ora} col formatore {self.formatore.username}, #{self.id}'