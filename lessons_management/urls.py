from django.urls import path
from . import views

urlpatterns = [
    path('list', views.UserHubList.as_view(), name='list_hub'),
    # LESSONS
    path('lessons/detail/<int:pk>', views.LessonDetail.as_view(), name='detail_lesson'),
    path('lessons/add', views.CreateLesson.as_view(), name='create_lesson'),
    path('lessons/remove/<int:pk>', views.DeleteLesson.as_view(), name='delete_lesson'),
    path('lessons/edit/<int:pk>', views.UpdateLesson.as_view(), name='update_lesson'),
    # PACKETS
    path('packets/detail/<int:pk>', views.PacketDetail.as_view(), name='detail_pacekt'),
    path('packets/add', views.CreatePacket.as_view(), name='create_packet'),
    path('packets/remove/<int:pk>', views.DeletePacket.as_view(), name='delete_packet'),
    path('packets/edit/<int:pk>', views.UpdatePacket.as_view(), name='update_packet'),
    # COURSES
    path('courses/detail/<int:pk>', views.CourseDetail.as_view(), name='detail_course'),
    path('courses/add', views.CreateCourse.as_view(), name='create_course'),
    path('courses/remove/<int:pk>', views.DeleteCourse.as_view(), name='delete_course'),
    path('courses/edit/<int:pk>', views.UpdateCourse.as_view(), name='update_course'),
]
