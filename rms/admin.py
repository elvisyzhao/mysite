# coding: UTF-8
from django.contrib import admin
from .models import Player, Restaurant, DishType, Dish
import logging
from django import forms
from .models import Order, OrderEntry
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class RMSAdminSite(AdminSite):
    site_header = "餐馆管理系统"

class DishTypeInline(admin.TabularInline):
    model = DishType

class DishInline(admin.TabularInline):
    model = Dish
    show_change_link = True
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dish_type" and request.__obj__:
            logger.error(db_field)
            kwargs['queryset'] = request.__obj__.dishtype_set.all() 
        return super(DishInline, self).formfield_for_foreignkey(db_field,
                request, **kwargs)

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [DishTypeInline, DishInline]
    def get_form(self, request, obj=None, **kwargs):
        request.__obj__ = obj
        return super(RestaurantAdmin, self).get_form(request, obj, **kwargs)

class OrderEntryInline(admin.TabularInline):
    model = OrderEntry

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]

class PlayerInline(admin.TabularInline):
    model = Player
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines=[PlayerInline]
    
admin_site = RMSAdminSite(name="rmsadmin")

admin_site.register(Restaurant, RestaurantAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(User, UserAdmin)
