from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    USERNAME_FIELD = None # Per evitare il problema per cui Profile non ha il campo USERNAME_FIELD
    # foto profilo dell'utente
    foto = models.ImageField(upload_to='user_photo/', default="uploaded_files/media/user_db/user_photo/None/none_picture.png")
    saldo = models.FloatField(default=130.0)

    def __str__(self):
        return f'profile user di: {self.user.username} (id: {self.user.id})'

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()