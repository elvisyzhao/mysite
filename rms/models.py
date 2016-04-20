# coding: UTF-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import pytz

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    def __unicode__(self):
        return self.user.username

class Restaurant(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

class DishType(models.Model):
    name = models.CharField(max_length=32)
    restaurant = models.ForeignKey(Restaurant)
    def __unicode__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=32)
    dish_type = models.ForeignKey(DishType)
    restaurant = models.ForeignKey(Restaurant)
    photo = models.ImageField()
    price = models.IntegerField()
    def __unicode__(self):
        return self.name

class Order(models.Model):
    INITIALIZED = 'ID'
    PAID = 'PD'
    CANCELED = 'CD'
    REFUNDING = 'RG'
    REFUNDED = 'RD'
    FINISHED = 'FD'
    STATUS_CHOICE = (
            (INITIALIZED, u'未支付'),
            (PAID, u'已支付'),
            (CANCELED, u'已取消'),
            (REFUNDING, u'退款中'),
            (REFUNDED, u'已退款'),
            (FINISHED, u'已完成')
            )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Player, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    order_time = models.DateTimeField(auto_now_add=True)
    extras = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=16)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE,
            default=INITIALIZED)

    def _get_total_price(self):
        total_price = 0
        for entry in self.orderentry_set.all():
            total_price += entry.count * entry.dish.price
        return total_price
    price = property(_get_total_price)

    def __unicode__(self):
        tz = pytz.timezone('Asia/Shanghai')
        return self.appointment_time.astimezone(tz).strftime('%y-%m-%d %H:%M')

class OrderEntry(models.Model):
    dish = models.ForeignKey(Dish)
    count = models.IntegerField()
    order = models.ForeignKey(Order)

    def __unicode__(self):
        return self.dish.name + unicode(self.count)

