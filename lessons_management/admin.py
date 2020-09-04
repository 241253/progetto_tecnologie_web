from django.contrib import admin
from lessons_management.models import Lesson, Packet, UserPackets

admin.site.register(Lesson)
admin.site.register(Packet)
admin.site.register(UserPackets)
