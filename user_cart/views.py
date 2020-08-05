from django.shortcuts import render
from django.views.generic.base import View
from user_cart.models import Cart, CartDetail


# def login_redirect(request):
#     if request.user.is_staff:
#         return render(request, 'user_management/staff/staff_page.html')
#     else:
#         return render(request, 'landingPage.html')

# cart_id = None
# for cart in carts:
#     if cart.user_id == request.user.id:
#         cart_id = cart.id
#         break

class AddToCart(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['id']
        product_type = self.kwargs['type']

        cart = None
        if len(Cart.objects.filter(user_id=request.user.id)) == 1:
            cart = Cart.objects.filter(user_id=request.user.id)[0]
        else:
            cart = Cart.objects.create(user_id=request.user.id)
            cart.save()

        if len(CartDetail.objects.filter(cart_id=cart.id, product_id=product_id, product_type=product_type)) != 1:
            cart_detail = CartDetail.objects.create(cart_id=cart.id, product_id=product_id, product_type=product_type)
            cart_detail.save()
            return render(request, 'user_cart/cart_succes.html')
        else:
            return render(request, 'user_cart/cart_error.html')

