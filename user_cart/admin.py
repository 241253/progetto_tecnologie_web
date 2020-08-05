from django.contrib import admin

# Register your models here.
from user_cart.models import Cart, CartDetail

admin.site.register(Cart)
admin.site.register(CartDetail)