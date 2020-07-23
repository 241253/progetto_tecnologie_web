from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Lesson(models.Model):

    GENRE_CHOICES = (('PC', 'Punta e clicca'), ('A', 'Avventura'), ('GM', 'Gioco matematico'), ('ST', 'Story-telling'), ('GV', 'Giochi vocali'), ('R', 'Racing'), ('A', 'Altro...'))
    DIFFICULTY_CHOICES = (('FB','Facile - base'), ('FA', 'Facile - avanzato'), ('MB', 'Media - base'), ('MA', 'Media - avanzata'), ('DB', 'Difficile - base'), ('DA', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=300)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='FB')
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, default='A')
    price = models.FloatField(default=20.0)
    video = models.FileField(upload_to='gallery', default='uploaded_files/media/user_db/user_photo/None/none_picture.png') #videolezione

    # @receiver(post_save, sender=User)
    # def create_user_lesson(sender, instance, created, **kwargs):
    #     if created:
    #         Lesson.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_lesson(sender, instance, **kwargs):
    #     instance.profile.save()