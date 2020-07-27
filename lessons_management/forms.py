from django import forms
from lessons_management.models import Lesson, Packet, Course


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
def getLessonsChoices():
    choices = list()
    for lesson in Lesson.objects.all():
        choices.append((lesson.id, f'Lezione: {lesson.title}'))
    return choices

class PacketCreationForm(forms.ModelForm):

    choices = getLessonsChoices()
    lessons = forms.MultipleChoiceField(choices=choices)
    
    class Meta:
        model = Packet
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(PacketCreationForm, self).__init__(*args, **kwargs)

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
        packet = super(PacketCreationForm, self).save(commit=False)
        packet.user_id = self.current_user.id

        difficulty = 0.0
        price = 0.0
        for lesson_id in self.cleaned_data['lessons']:
            lesson = Lesson.objects.filter(id=lesson_id)[0]
            difficulty += float(lesson.difficulty)
            price += lesson.price
        difficulty /= len(self.cleaned_data['lessons'])

        packet.difficulty = self.normalize_difficulty(difficulty)
        packet.price = price*0.80

        if commit:
            packet.save()
            packet.lessons.set([int(lesson_id) for lesson_id in self.cleaned_data['lessons']])
        return packet

class PacketUpdateForm(forms.ModelForm):

    choices = getLessonsChoices()
    lessons = forms.MultipleChoiceField(choices=choices)

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
        price = 0.0
        for lesson_id in self.cleaned_data['lessons']:
            lesson = Lesson.objects.filter(id=lesson_id)[0]
            difficulty += float(lesson.difficulty)
            price += lesson.price
        difficulty /= len(self.cleaned_data['lessons'])

        packet.difficulty = self.normalize_difficulty(difficulty)
        packet.price = price*0.80

        # print(self.fields['lessons'])mi piglio il campo lessons (devo vedere se posso usarlo)

        if commit:
            packet.save()
            packet.lessons.set([int(lesson_id) for lesson_id in self.cleaned_data['lessons']])
        return packet


# COURSES
def getPacketChoices():
    choices = list()
    for packet in Packet.objects.all():
        choices.append((packet.id, f'Pacchetto: {packet.title}'))
    return choices


class CourseCreationForm(forms.ModelForm):
    choices = getPacketChoices()
    packets = forms.MultipleChoiceField(choices=choices)

    class Meta:
        model = Course
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(CourseCreationForm, self).__init__(*args, **kwargs)

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
        course = super(CourseCreationForm, self).save(commit=False)
        course.user_id = self.current_user.id

        difficulty = 0.0
        price = 0.0
        for packet_id in self.cleaned_data['packets']:
            packet = Packet.objects.filter(id=packet_id)[0]
            difficulty += float(packet.difficulty)
            price += packet.price
        difficulty /= len(self.cleaned_data['packets'])

        course.difficulty = self.normalize_difficulty(difficulty)
        course.price = price * 0.75

        if commit:
            course.save()
            course.packets.set([int(packet_id) for packet_id in self.cleaned_data['packets']])
        return course


class CourseUpdateForm(forms.ModelForm):
    choices = getPacketChoices()
    packets = forms.MultipleChoiceField(choices=choices)

    class Meta:
        model = Course
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
        course = super(CourseUpdateForm, self).save(commit=False)

        difficulty = 0.0
        price = 0.0
        for packet_id in self.cleaned_data['packets']:
            packet = Packet.objects.filter(id=packet_id)[0]
            difficulty += float(packet.difficulty)
            price += packet.price
        difficulty /= len(self.cleaned_data['packets'])

        # print(self.fields['packet'])mi piglio il campo packets (devo vedere se posso usarlo)

        course.difficulty = self.normalize_difficulty(difficulty)
        course.price = price * 0.75

        if commit:
            course.save()
            course.packets.set([int(packet_id) for packet_id in self.cleaned_data['packets']])
        return course