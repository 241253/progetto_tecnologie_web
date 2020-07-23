from django.urls import path
from . import views

urlpatterns = [
    path('list', views.LessonUserList.as_view(), name='lessons_list'),
    path('add', views.CreateLesson.as_view(), name='create_lesson'),
]
