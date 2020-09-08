from django import forms
from lessons_management.models import Lesson, Packet, UserPackets

# LESSONS
class LessonsCreationForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'difficulty', 'genre', 'price', 'video')
        labels = {'title': 'Titolo', 'description':'Descrizione','difficulty':'Difficoltà','genre':'Genere','price':'Prezzo','video':'Video'}

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(LessonsCreationForm, self).__init__(*args, **kwargs)
        self.fields['video'].label = "Video"
        self.fields['video'].required = True

    def save(self, commit=True):
        lesson = super(LessonsCreationForm, self).save(commit=False)
        lesson.user_id = self.current_user.id
        if commit:
            lesson.save()
        return lesson

class LessonsUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'difficulty', 'genre', 'price', 'video')
        labels = {'title': 'Titolo', 'description':'Descrizione','difficulty':'Difficoltà','genre':'Genere','price':'Prezzo','video':'Video'}

# PACKETS
def getLessonsChoices():
    choices = list()
    for lesson in Lesson.objects.all():
        choices.append((lesson.id, f'Lezione: {lesson.title}'))
    return choices

class PacketCreationForm(forms.ModelForm):
    choices = getLessonsChoices()
    lessons = forms.MultipleChoiceField(choices=choices, label='Lezioni')
    
    class Meta:
        model = Packet
        fields = ('title', 'description')
        labels = {'title':'Titolo', 'description':'Descrizione'}

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(PacketCreationForm, self).__init__(*args, **kwargs)
        self.fields['lessons'].choices = getLessonsChoices()

    def normalize_difficulty(self, difficulty):
        if difficulty < 1.5:
            difficulty = '1.0'
        elif 1.5 <= difficulty < 2.5:
            difficulty = '2.0'
        elif 2.5 <= difficulty < 3.5:
            difficulty = '3.0'
        elif 3.5 <= difficulty < 4.5:
            difficulty = '4.0'
        elif 4.5 <= difficulty < 5.5:
            difficulty = '5.0'
        else:
            difficulty = '6.0'
        return difficulty

    def clean_lessons(self):
        lessons = self.cleaned_data['lessons']
        if len(lessons) < 5:
            raise forms.ValidationError('Devi selezionare almeno 5 lezioni!')
        return lessons

    def save(self, commit=True):
        packet = super(PacketCreationForm, self).save(commit=False)
        packet.user_id = self.current_user.id

        difficulty = 0.0
        for lesson_id in self.cleaned_data['lessons']:
            lesson = Lesson.objects.get(id=lesson_id)
            difficulty += float(lesson.difficulty)
        difficulty /= len(self.cleaned_data['lessons'])

        packet.difficulty = self.normalize_difficulty(difficulty)

        if commit:
            packet.save()
            packet.lessons.set([int(lesson_id) for lesson_id in self.cleaned_data['lessons']])
        return packet

class PacketUpdateForm(forms.ModelForm):

    choices = getLessonsChoices()
    lessons = forms.MultipleChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        super(PacketUpdateForm, self).__init__(*args, **kwargs)
        self.fields['lessons'].choices = getLessonsChoices()

    class Meta:
        model = Lesson
        fields = ('title', 'description')

    def normalize_difficulty(self, difficulty):
        if difficulty < 1.5:
            difficulty = '1.0'
        elif 1.5 <= difficulty < 2.5:
            difficulty = '2.0'
        elif 2.5 <= difficulty < 3.5:
            difficulty = '3.0'
        elif 3.5 <= difficulty < 4.5:
            difficulty = '4.0'
        elif 4.5 <= difficulty < 5.5:
            difficulty = '5.0'
        else:
            difficulty = '6.0'
        return difficulty

    def save(self, commit=True):
        packet = super(PacketUpdateForm, self).save(commit=False)

        difficulty = 0.0
        for lesson_id in self.cleaned_data['lessons']:
            lesson = Lesson.objects.filter(id=lesson_id)[0]
            difficulty += float(lesson.difficulty)
        difficulty /= len(self.cleaned_data['lessons'])

        packet.difficulty = self.normalize_difficulty(difficulty)

        if commit:
            packet.save()
            packet.lessons.set([int(lesson_id) for lesson_id in self.cleaned_data['lessons']])
        return packet

#USER PACKETS
class UserPacketsCreationForm(forms.ModelForm):
    class Meta:
        model = UserPackets
        exclude = ['user', 'packet']

    def __init__(self, *args, **kwargs):
        self.packet_id = kwargs.pop('packet_id')
        self.user = kwargs.pop('user')
        super(UserPacketsCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user_packets = super(UserPacketsCreationForm, self).save(commit=False)

        user_packets.user = self.user
        user_packets.packet = Packet.objects.get(id=self.packet_id)

        if commit:
            user_packets.save()
        return user_packets

class UserPacketsDeleteForm(forms.ModelForm):
    class Meta:
        model = UserPackets
        exclude = ['user', 'packet']

    def is_valid(self):
        return True