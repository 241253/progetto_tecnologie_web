from django.urls import path
from . import views

urlpatterns = [
    path('list', views.UserHubList.as_view(), name='list_hub'),
    # LESSONS
    path('lessons/add', views.CreateLesson.as_view(), name='create_lesson'),
    path('lessons/remove/<int:pk>', views.DeleteLesson.as_view(), name='delete_lesson'),
    path('lessons/edit/<int:pk>', views.UpdateLesson.as_view(), name='update_lesson'),
    # PACKETS
    path('packets/add', views.CreatePacket.as_view(), name='create_packet'),
    path('packets/remove/<int:pk>', views.DeletePacket.as_view(), name='delete_packet'),
    path('packets/edit/<int:pk>', views.UpdatePacket.as_view(), name='update_packet'),
]
