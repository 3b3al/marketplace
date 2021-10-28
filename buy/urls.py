  
from django.conf.urls import url
from buy.models import Customer
from django.urls import path
from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
     url(r'^login/$', views.login , name='login'),
     url(r'^login/login$', views.login , name='login'),
     url(r'^logout$', views.logout , name='logout'),
     #url('buy', views.order),
     url(r'^remove$', views.remove , name='remove'),
     url(r'^quantity$', views.quantity , name='item_quantity'),
     url(r'^$', views.index , name='home_page'),
     url(r'^index$', views.index , name='home_page'),
     url(r'^register$', views.register , name='register'),
     url(r'^showitem/(?P<slug>[-\w]+)/$', views.showitem , name='item_detail'),
     url(r'^all_items$', views.all_items , name='all_items'),
     url(r'^add$', views.add , name='add_item'),
     url(r'^cart$', views.cart , name='cart'),
     #url(r'^cart/(?P<slug>[-\w]+)/$', views.cart_add , name='cart_add'),
     url(r'^order$', views.order , name='confirm_order'),
     url(r'^success$', views.success , name='order_success'),
     url(r'^contact$', views.contact_view , name='contact'),
     url(r'^aboutus$', views.about_us, name='about_us'),
     url(r'^policy$', views.privacy_policy , name='policy'),
     url(r'^terms$', views.terms , name='terms'),
     url(r'^account$', views.myacc , name='my_account')

     #url('search', views.search),
    
 ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)