from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from lessons_management.forms import LessonsCreationForm, LessonsUpdateForm, PacketCreationForm, PacketUpdateForm, \
    CourseUpdateForm, CourseCreationForm
from lessons_management.models import Lesson, Packet, Course
from user_cart.models import PurchasedLessons


@method_decorator(login_required, name='dispatch')
class UserHubList(ListView):
    model = Lesson
    template_name = 'lessons_management/list_hub.html'

    def get_context_data(self, **kwargs):
        context = super(UserHubList, self).get_context_data(**kwargs)
        context.update({
            'lesson_list': Lesson.objects.order_by('title'),
            'packet_list': Packet.objects.all(),
            'course_list': Course.objects.all(),
        })
        return context

# LESSONS
@method_decorator(login_required, name='dispatch')
class CreateLesson(CreateView):
    model = Lesson
    form_class = LessonsCreationForm
    template_name = 'lessons_management/lessons/create_lesson.html'
    success_url = reverse_lazy('list_hub')

    def get_form_kwargs(self):
        kwargs = super(CreateLesson, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator(login_required, name='dispatch')
class DeleteLesson(DeleteView):
    model = Lesson
    template_name = 'lessons_management/lessons/delete_lesson.html'
    success_url = reverse_lazy('list_hub')

@method_decorator(login_required, name='dispatch')
class UpdateLesson(UpdateView):
    model = Lesson
    form_class = LessonsUpdateForm
    template_name = 'lessons_management/lessons/update_lesson.html'
    success_url = reverse_lazy('list_hub')

class LessonDetail(DeleteView):
    template_name = 'lessons_management/lessons/detail_lesson.html'
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super(LessonDetail, self).get_context_data(**kwargs)
        purchasedLessons = []
        for pl in PurchasedLessons.objects.filter(user_id=self.request.user.id):
            purchasedLessons.append(pl.lesson.id)
        context['purchased_item'] = purchasedLessons
        return context

# PACKETS
@method_decorator(login_required, name='dispatch')
class CreatePacket(CreateView):
    model = Packet
    form_class = PacketCreationForm
    template_name = 'lessons_management/packets/create_packet.html'
    success_url = reverse_lazy('list_hub')

    def get_form_kwargs(self):
        kwargs = super(CreatePacket, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@method_decorator(login_required, name='dispatch')
class DeletePacket(DeleteView):
    model = Packet
    template_name = 'lessons_management/packets/delete_packet.html'
    success_url = reverse_lazy('list_hub')



@method_decorator(login_required, name='dispatch')
class UpdatePacket(UpdateView):
    model = Packet
    form_class = PacketUpdateForm
    template_name = 'lessons_management/packets/update_packet.html'
    success_url = reverse_lazy('list_hub')

class PacketDetail(DeleteView):
    template_name = 'lessons_management/packets/detail_packet.html'
    model = Packet

# COURSES
@method_decorator(login_required, name='dispatch')
class CreateCourse(CreateView):
    model = Packet
    form_class = CourseCreationForm
    template_name = 'lessons_management/course/create_course.html'
    success_url = reverse_lazy('list_hub')

    def get_form_kwargs(self):
        kwargs = super(CreateCourse, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator(login_required, name='dispatch')
class DeleteCourse(DeleteView):
    model = Course
    template_name = 'lessons_management/course/delete_course.html'
    success_url = reverse_lazy('list_hub')

@method_decorator(login_required, name='dispatch')
class UpdateCourse(UpdateView):
    model = Course
    form_class = CourseUpdateForm
    template_name = 'lessons_management/course/update_course.html'
    success_url = reverse_lazy('list_hub')

class CourseDetail(DeleteView):
    template_name = 'lessons_management/course/detail_course.html'
    model = Course