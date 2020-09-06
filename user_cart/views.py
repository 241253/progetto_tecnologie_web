from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView
from lessons_management.models import Lesson
from user_cart.models import Cart, CartDetail, PurchasedLessons
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from user_management.models import Profile

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class RemoveToCart(DeleteView):
        model = CartDetail
        template_name = 'user_cart/cart_remove.html'
        success_url = reverse_lazy('cart')

        def get_context_data(self, **kwargs):
            context = super(RemoveToCart, self).get_context_data(**kwargs)
            lesson = Lesson.objects.get(id=context['cartdetail'].product_id)
            context.update({'lesson_title':lesson.title})
            print(lesson.title)
            return context

@method_decorator(login_required, name='dispatch')
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
            sconto = 0
            if len(lessons) != 0:
                for lesson in lessons:
                    totale += lesson.price
                sconto = int(len(lessons)/5)

            context.update({
                'lessons': lessons,
                'totale': totale,
                'cart_details': cart_details,
            })
            if sconto != 0:
                context.update({
                    'sconto': 'si',
                    'totale_scontato': totale - sconto * 20,
                })
            else:
                context.update({'sconto': 'no',})
            return context

@method_decorator(login_required, name='dispatch')
class PurchaseConfirmView(TemplateView):
    template_name = "user_cart/purchase_confirm.html"

    def get_context_data(self, **kwargs):
        context = super(PurchaseConfirmView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user.id)
        cart_details = CartDetail.objects.all().filter(cart=cart.id)
        lessons = Lesson.objects.filter(id__in=[cart_detail.product_id for cart_detail in cart_details])
        totale = 0.0
        totale_scontato = 0.0
        sconto = False
        if len(lessons) != 0:
            count = 1
            for lesson in lessons:
                totale += lesson.price
                if count == 5:
                    totale_scontato += totale*0.8
                    count = 1
                    sconto = True
                else:
                    count += 1

        context.update({
            'lessons': lessons,
            'totale': totale,
            'cart_details': cart_details,
        })
        if sconto:
            context.update({
                'sconto': 'si',
                'totale_scontato': totale_scontato,
            })
        else:
            context.update({'sconto': 'no',})

        saldo = Profile.objects.get(user=self.request.user.id).saldo

        if saldo >= totale:
            context.update({'saldoSufficiente': 'si',})
        else:
            context.update({'saldoSufficiente': 'no',})

        return context

@method_decorator(login_required, name='dispatch')
class PurchaseSuccessView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user.id)
        cart_details = CartDetail.objects.all().filter(cart=cart.id)

        totale = 0.0
        for cart_detail in cart_details:
            l = Lesson.objects.get(id=cart_detail.product_id)
            totale += l.price
            pl = PurchasedLessons.objects.create(user=request.user, lesson=l)
            pl.save()
        profile = Profile.objects.get(user_id=request.user.id)
        profile.saldo -= totale
        profile.save()

        cart_details.delete()

        return render(request, 'user_cart/purchase_success.html')