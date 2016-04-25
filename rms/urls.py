from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url('^menu/([0-9]+)/$', views.menu),
        url('^pre_order/$', views.pre_order),
        url('^order/$', views.order),
        url('^show_order/([0-9]+)/$', views.show_order),
        url('^order_list/$', views.order_list),
        url('^get_code/$', views.get_code),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
