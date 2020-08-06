from django.contrib.auth.models import User
from django.db import models

from lessons_management.models import Lesson


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def product_count(self):
        cart_details = CartDetail.objects.all().filter(cart=self.id)
        lesson = Lesson.objects.filter(id__in=[cart_detail.product_id for cart_detail in cart_details])
        return len(lesson)

    def __str__(self):
        return f'{self.user.username} - Cart_id: {self.id}'

class CartDetail(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product_id = models.IntegerField()

    def __str__(self):
        return f'id: {self.id} - Cart_id: {self.cart.id} - Product_id: {self.product_id}'

class PurchasedLessons(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'id: {self.id} - Lesson_title: {self.lesson.title} - User_name: {self.user.username} - # {self.lesson.id} - # {self.user.id}'