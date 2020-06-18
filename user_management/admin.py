from django.contrib import admin

# Register your models here.

from user_management.models import User
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    list_display = ("email", "username", "nome", "cognome", "last_login", "is_admin", "is_staff", "is_active")
    search_fields = ("email", "username", "nome", "cognome")
    readonly_fields = ("last_login",)
    add_fieldsets = ((None, {"classes": ("wide", ), "fields": ("email", "username", "nome", "cognome", "password1", "password2"), }), )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ('email',)  # In questo modo l'ordering è su email e non su username come di default

admin.site.register(User, MyUserAdmin)