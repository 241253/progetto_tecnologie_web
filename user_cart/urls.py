from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:id>/', views.AddToCart.as_view(), name='cart_add'),
    path('cart/', views.CartView.as_view(), name='cart'),
]
