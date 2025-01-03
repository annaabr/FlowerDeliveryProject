from django.db import models
from django.contrib.auth.models import User
from goods.models import Flower


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)