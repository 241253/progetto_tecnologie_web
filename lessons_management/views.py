from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from lessons_management.models import Lesson


@method_decorator(login_required, name='dispatch')
class LessonUserList(ListView):
    model = Lesson
    template_name = 'lessons_management/lesson_list.html'

@method_decorator(login_required, name='dispatch')
class CreateLesson(CreateView):
    model = Lesson
    template_name = 'lessons_management/create_lesson.html'
    success_url = reverse_lazy('lessons_list')
    fields = ['title', 'description', 'difficulty', 'genre', 'price']
