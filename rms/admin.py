# coding: UTF-8
from django.contrib import admin
from .models import MyUser, Restaurant, DishType, Dish
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
    login_template = 'admin_login.html'
    #login_form = ''
    
    def login(self, request, extra_context=None):
        input_veri_code = request.POST.get('veri_code', None)
        veri_code = request.session.get('veri_code', None)
        phone = request.session.get('veri_phone', '')
        input_phone = request.POST.get('username', None)
        logger.error('input_phone is %s input_veri_code is %s phone is %s veri_code is %s' % (input_phone, input_veri_code, phone, veri_code))
        logger.error('next url is %s' % request.POST.get('next', '1111111'))
        if veri_code and input_veri_code and veri_code == input_veri_code:
            if input_phone == phone: 
                user, created = User.objects.get_or_create(username=phone)
                user.set_password('test')
                user.is_active = True
                user.is_superuser = True
                user.is_staff = True
                user.save()
                logger.error('user_created')
                request.POST._mutable = True
                request.POST['password'] = 'test'
                request.POST._mutable = False
                logger.error(request.POST['password'])
                return super(RMSAdminSite, self).login(request, extra_context)
        return super(RMSAdminSite, self).login(request, extra_context)

class DishTypeInline(admin.TabularInline):
    model = DishType

class DishInline(admin.TabularInline):
    model = Dish
    show_change_link = True
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dish_type" and request.__obj__:
             
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

class MyUserInline(admin.TabularInline):
    model = MyUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines=[MyUserInline]
    
admin_site = RMSAdminSite(name="rmsadmin")

admin_site.register(Restaurant, RestaurantAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(User, UserAdmin)
