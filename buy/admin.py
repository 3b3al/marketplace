from django.contrib import admin
from .models import *
# Register your models here.

    
admin.site.register(Customer )
admin.site.register(Item )
admin.site.register(MyOrder)
admin.site.register(OrderQuantity )