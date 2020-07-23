from django import forms
from lessons_management.models import Lesson


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