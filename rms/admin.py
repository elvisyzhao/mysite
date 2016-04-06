from django.contrib import admin
from .models import Owner, Restaurant, DishType, Dish
import logging
from django import forms
from .models import Order, OrderEntry

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

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

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Order, OrderAdmin)
