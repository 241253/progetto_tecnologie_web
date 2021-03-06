from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension

class Lesson(models.Model):

    GENRE_CHOICES = (('PC', 'Punta e clicca'), ('A', 'Avventura'), ('GM', 'Gioco matematico'), ('ST', 'Story-telling'), ('GV', 'Giochi vocali'), ('R', 'Racing'), ('AL', 'Altro...'))
    DIFFICULTY_CHOICES = (('1.0','Facile - base'), ('2.0', 'Facile - avanzato'), ('3.0', 'Media - base'), ('4.0', 'Media - avanzata'), ('5.0', 'Difficile - base'), ('6.0', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.SET(1), null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='1.0')
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, default='A')
    price = models.FloatField(default=20.0)
    video = models.FileField(upload_to='video_lessons', validators=[validate_file_extension])

    def __str__(self):
        return f'#{self.id} - {self.title}'

class Packet(models.Model):
    DIFFICULTY_CHOICES = (('1.0','Facile - base'), ('2.0', 'Facile - avanzato'), ('3.0', 'Media - base'), ('4.0', 'Media - avanzata'), ('5.0', 'Difficile - base'), ('6.0', 'Difficile - avanzata'))

    user = models.ForeignKey(User, on_delete=models.SET(1), null=True)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='1.0')
    lessons = models.ManyToManyField(Lesson)

    def set_normalize_difficulty(self):
        difficulty = sum([float(lesson.difficulty) for lesson in self.lessons.all()])/len(self.lessons.all())
        if difficulty < 1.5:
            self.difficulty = '1.0'
        elif 1.5 <= difficulty < 2.5:
            self.difficulty = '2.0'
        elif 2.5 <= difficulty < 3.5:
            self.difficulty = '3.0'
        elif 3.5 <= difficulty < 4.5:
            self.difficulty = '4.0'
        elif 4.5 <= difficulty < 5.5:
            self.difficulty = '5.0'
        else:
            self.difficulty = '6.0'
        self.save()

    @property
    def lessons_count(self):
        return self.lessons.all().count()

    def __str__(self):
        return f'#{self.id} - {self.title}'

class UserPackets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.id} - {self.user.username} - pacchetto: {self.packet.title}'
