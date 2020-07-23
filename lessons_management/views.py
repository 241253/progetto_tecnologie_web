from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from lessons_management.forms import LessonsCreationForm, LessonsUpdateForm
from lessons_management.models import Lesson


@method_decorator(login_required, name='dispatch')
class LessonUserList(ListView):
    model = Lesson
    template_name = 'lessons_management/lesson_list.html'

@method_decorator(login_required, name='dispatch')
class CreateLesson(CreateView):
    model = Lesson
    form_class = LessonsCreationForm
    template_name = 'lessons_management/create_lesson.html'
    success_url = reverse_lazy('lessons_list')

    def get_form_kwargs(self):
        kwargs = super(CreateLesson, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator(login_required, name='dispatch')
class DeleteLesson(DeleteView):
    model = Lesson
    template_name = 'lessons_management/delete_lesson.html'
    success_url = reverse_lazy('lessons_list')

@method_decorator(login_required, name='dispatch')
class UpdateLesson(UpdateView):
    model = Lesson
    form_class = LessonsUpdateForm
    template_name = 'lessons_management/update_lesson.html'
    success_url = reverse_lazy('lessons_list')