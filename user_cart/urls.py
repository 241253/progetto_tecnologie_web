from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:id>/<slug:type>/', views.AddToCart.as_view(), name='cart_add'),
]
