from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateField()
    menu = models.ForeignKey(
        to=Menu, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {} {}'.format(self.order_date, self.user.username,
                                 self.menu.name)

    class Meta:
        unique_together = ('order_date', 'menu', 'user')
