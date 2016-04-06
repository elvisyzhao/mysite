from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import pytz

class Owner(models.Model):
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user.username

class Restaurant(models.Model):
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
    appointment_time = models.DateTimeField()
    order_time = models.DateTimeField(auto_now_add=True)
    extras = models.CharField(max_length=128, null=True)
    def __unicode__(self):
        tz = pytz.timezone('Asia/Shanghai')
        return self.appointment_time.astimezone(tz).strftime('%y-%m-%d %H:%M')

class OrderEntry(models.Model):
    dish = models.ForeignKey(Dish)
    count = models.IntegerField()
    order = models.ForeignKey(Order)

    def __unicode__(self):
        return self.dish.name + unicode(self.count)

