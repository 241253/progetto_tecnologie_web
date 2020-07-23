from django.urls import path
from . import views

urlpatterns = [
    path('list', views.LessonUserList.as_view(), name='lessons_list'),
    path('add', views.CreateLesson.as_view(), name='create_lesson'),
    path('remove/<int:pk>', views.DeleteLesson.as_view(), name='delete_lesson'),
    path('edit/<int:pk>', views.UpdateLesson.as_view(), name='update_lesson'),
]
