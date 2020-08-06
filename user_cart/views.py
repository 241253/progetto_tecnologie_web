from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic.base import View, TemplateView

from lessons_management.models import Lesson
from user_cart.models import Cart, CartDetail

class AddToCart(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['id']

        cart = None
        if len(Cart.objects.filter(user_id=request.user.id)) == 1:
            cart = Cart.objects.filter(user_id=request.user.id)[0]
        else:
            cart = Cart.objects.create(user_id=request.user.id)
            cart.save()

        if len(CartDetail.objects.filter(cart_id=cart.id, product_id=product_id)) != 1:
            cart_detail = CartDetail.objects.create(cart_id=cart.id, product_id=product_id)
            cart_detail.save()
            return render(request, 'user_cart/cart_succes.html')
        else:
            return render(request, 'user_cart/cart_error.html')


# class RemoveToCart(View):
#
#     def get(self, request, *args, **kwargs):
#         product_id = self.kwargs['id']
#
#         cart = None
#         if len(Cart.objects.filter(user_id=request.user.id)) == 1:
#             cart = Cart.objects.filter(user_id=request.user.id)[0]
#         else:
#             cart = Cart.objects.create(user_id=request.user.id)
#             cart.save()
#
#         if len(CartDetail.objects.filter(cart_id=cart.id, product_id=product_id)) != 1:
#             cart_detail = CartDetail.objects.create(cart_id=cart.id, product_id=product_id)
#             cart_detail.save()
#             return render(request, 'user_cart/cart.html')
#         else:
#             return render(request, 'user_cart/cart_error.html')

class CartView(TemplateView):
    template_name = 'user_cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(user=self.request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.request.user)
            cart.save()
        finally:
            cart_details = CartDetail.objects.all().filter(cart=cart.id)
            lessons = Lesson.objects.filter(id__in=[cart_detail.product_id for cart_detail in cart_details])
            totale = 0.0
            sconto = False
            if len(lessons) != 0:
                count = 1
                for lesson in lessons:
                    totale += lesson.price
                    if count == 5:
                        totale *= 0.8
                        count = 1
                        sconto = True
                    else:
                        count += 1

            context.update({
                'lessons': lessons,
                'totale': totale,
            })
            if sconto:
                context.update({'sconto': 'si',})
            else:
                context.update({'sconto': 'no',})
            return context
