from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Lesson(models.Model):

    GENRE_CHOICES = (('PC', 'Punta e clicca'), ('A', 'Avventura'), ('GM', 'Gioco matematico'), ('ST', 'Story-telling'), ('GV', 'Giochi vocali'), ('R', 'Racing'), ('A', 'Altro...'))
    DIFFICULTY_CHOICES = (('1.0','Facile - base'), ('2.0', 'Facile - avanzato'), ('3.0', 'Media - base'), ('4.0', 'Media - avanzata'), ('5.0', 'Difficile - base'), ('6.0', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=300)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='1.0')
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, default='A')
    price = models.FloatField(default=20.0)
    video = models.FileField(upload_to='gallery', default='uploaded_files/media/user_db/user_photo/None/none_picture.png') #videolezione

    def __str__(self):
        return f'#{self.id} - {self.title}'

class Packet(models.Model):
    DIFFICULTY_CHOICES = (('1.0','Facile - base'), ('2.0', 'Facile - avanzato'), ('3.0', 'Media - base'), ('4.0', 'Media - avanzata'), ('5.0', 'Difficile - base'), ('6.0', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=300)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='1.0')
    price = models.FloatField(default=100.0)
    lessons = models.ManyToManyField(Lesson)

    @property
    def lessons_count(self):
        return self.lessons.all().count()

    def __str__(self):
        return f'#{self.id} - {self.title}'

class Course(models.Model):
    DIFFICULTY_CHOICES = (
    ('1.0', 'Facile - base'), ('2.0', 'Facile - avanzato'), ('3.0', 'Media - base'), ('4.0', 'Media - avanzata'),
    ('5.0', 'Difficile - base'), ('6.0', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=300)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='1.0')
    price = models.FloatField(default=300.0)
    packets = models.ManyToManyField(Packet)

    @property
    def packets_count(self):
        return self.packets.all().count()

    def lessons_count(self):
        return sum([packet.lessons_count for packet in self.packets.all()])

    def __str__(self):
        return f'#{self.id} - {self.title}'
