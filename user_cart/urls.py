from django.urls import path
from . import views

urlpatterns = [
    #CART URL
    path('cart/add/<int:id>/', views.AddToCart.as_view(), name='cart_add'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/remove/<int:pk>/', views.RemoveToCart.as_view(), name='cart_remove'),
    #PURCHASEDLESSON URL
    path('cart/purchase/confirm', views.PurchaseConfirmView.as_view(), name='cart_purchase_confirm'),
    path('cart/purchase/success', views.PurchaseSuccessView.as_view(), name='cart_purchase_success'),
]
