from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from random import randint
import datetime
from django.utils.text import slugify
# Create your models here.


class Customer(models.Model):
    customer_first_name = models.CharField(max_length=100 , null=True)
    customer_last_name = models.CharField(max_length=100 , null=True)
    customer_email = models.EmailField(null=True)
    customer_phone = models.CharField(max_length=50)
    customer_address1 = models.TextField(null=True)
    customer_address2 = models.TextField(null=True)
    customer_password = models.CharField(max_length=255 , null=True)
    customer_created_at = models.DateTimeField(auto_now_add=True , null=True)
    customer_updated_at = models.DateTimeField(auto_now=True , null=True)

    # def __str__(self):
    #     return self .customer_email
    



        
class Item(models.Model):
    item_name = models.CharField(max_length=50 , null=True)
    item_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    item_description = models.TextField(null=True)
    item_summary = models.TextField(null=True)
    item_type = models.CharField(max_length=50, null=True)
    item_brand = models.CharField(max_length=50, null=True)
    item_weight = models.DecimalField(default=0.00, max_digits=100, decimal_places=3)
    item_picture = models.ImageField(default='images/0177.jpg', upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    slug    = models.SlugField(null=True , blank= True)

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.item_name)
        super(Item , self).save( *args , **kwargs)

    def __str__(self):
        return self .item_name



class MyOrder(models.Model):
    order_tracking_code = models.CharField(max_length = 15, null =True)
    order_customer_id = models.ForeignKey('Customer' , on_delete=models.CASCADE, null=True)
    order_first_name = models.CharField(max_length=50 , null=True)
    order_last_name = models.CharField(max_length=50 , null=True)
    order_email = models.EmailField(null=True)
    order_phone = models.CharField(max_length=50 , null=True)
    #ordered_item = models.ForeignKey('OrderQuantity', on_delete=models.CASCADE , null=True)
    order_address = models.TextField(null=True)
    order_payment_method = models.CharField(max_length = 30 , null=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True , null=True)
   # order_items = models.ManyToManyField('Item')
    order_total_price = models.DecimalField(default = 0.00, max_digits= 100, decimal_places=2)


    def __str__(self):
        return self.order_email


class OrderQuantity(models.Model):
    product = models.ForeignKey('Item' , on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)


  