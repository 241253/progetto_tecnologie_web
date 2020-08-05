from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} - Cart_id: {self.id}'

class CartDetail(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=1)

    def __str__(self):
        return f'id: {self.id} - Cart_id: {self.cart.id} - Product_id: {self.product_id} - {self.product_type}'