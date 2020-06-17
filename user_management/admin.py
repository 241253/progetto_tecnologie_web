from django.contrib import admin

# Register your models here.

from user_management.models import User
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    list_display = ("email", "nome", "cognome", "last_login", "is_admin", "is_staff", "is_active")
    search_fields = ("email", "nome", "cognome")
    readonly_fields = ("last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, MyUserAdmin)