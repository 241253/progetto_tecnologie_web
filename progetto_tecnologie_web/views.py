from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic.base import View, TemplateView

from lessons_management.models import Lesson, Packet, Course
from user_cart.models import PurchasedLessons


class HomePage(TemplateView):

    template_name = "homePage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        purchasedLessons = []
        for pl in PurchasedLessons.objects.filter(user_id=self.request.user.id):
            purchasedLessons.append(pl.lesson.id)
        context.update({
            'lesson_list_1': Lesson.objects.all().filter(difficulty=1.0),
            'lesson_list_2': Lesson.objects.all().filter(difficulty=2.0),
            'lesson_list_3': Lesson.objects.all().filter(difficulty=3.0),
            'lesson_list_4': Lesson.objects.all().filter(difficulty=4.0),
            'lesson_list_5': Lesson.objects.all().filter(difficulty=5.0),
            'lesson_list_6': Lesson.objects.all().filter(difficulty=6.0),
            'packet_list_1': Packet.objects.all().filter(difficulty=1.0),
            'packet_list_2': Packet.objects.all().filter(difficulty=2.0),
            'packet_list_3': Packet.objects.all().filter(difficulty=3.0),
            'packet_list_4': Packet.objects.all().filter(difficulty=4.0),
            'packet_list_5': Packet.objects.all().filter(difficulty=5.0),
            'packet_list_6': Packet.objects.all().filter(difficulty=6.0),
            'course_list_1': Course.objects.all().filter(difficulty=1.0),
            'course_list_2': Course.objects.all().filter(difficulty=2.0),
            'course_list_3': Course.objects.all().filter(difficulty=3.0),
            'course_list_4': Course.objects.all().filter(difficulty=4.0),
            'course_list_5': Course.objects.all().filter(difficulty=5.0),
            'course_list_6': Course.objects.all().filter(difficulty=6.0),
            'purchased_item': purchasedLessons
        })
        return context

@never_cache
def landingPage(request):
    return render(request, 'landingPage.html')

def reservationPage(request):
    return render(request, 'prenotazioni.html')

def pricesPage(request):
    return render(request, 'tariffe.html')

def chi_siamoPage(request):
    return render(request, 'chi_siamo.html')

def contacts(request):
    return render(request, 'contatti.html')

