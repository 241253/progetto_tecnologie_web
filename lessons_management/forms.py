from django import forms
from lessons_management.models import Lesson, Packet


# LESSONS

class LessonsCreationForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'difficulty', 'genre', 'price', 'video')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(LessonsCreationForm, self).__init__(*args, **kwargs)
        self.fields['video'].label = "Video"
        self.fields['video'].required = False

    def save(self, commit=True):
        lesson = super(LessonsCreationForm, self).save(commit=False)
        lesson.user_id = self.current_user.id
        if commit:
            lesson.save()
        return lesson

    # def clean_video(self): da implementare prima o poi

class LessonsUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'difficulty', 'genre', 'price', 'video')

    # def clean_video(self): da implementare prima o poi

# PACKETS

class PacketCreationForm(forms.ModelForm):
    class Meta:
        model = Packet
        fields = ('title', 'description')
        # fields = ('title', 'description', 'lessons')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(PacketCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        packet = super(PacketCreationForm, self).save(commit=False)
        packet.user_id = self.current_user.id
        packet.difficulty = '1.0'
        packet.price = 100
        if commit:
            packet.save()
        return packet

class PacketUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description')
        # fields = ('title', 'description', 'lessons')

