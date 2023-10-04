from datetime import datetime
from django.db import models
from accounts.models import User
from django.utils import timezone   
from store.models import Product, Variants, Variation
from vendor.models import Vendor

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    def num_of_items(self):
        cartitems = self.CareItem_set.all()
        qtysum = sum([ qty for qty in cartitems])
        return qtysum

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    variant = models.ForeignKey(Variants,on_delete=models.SET_NULL,blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now = True)
    

    

    def __unicode__(self):
        return self.product
    
    @property
    def sub_total(self):
        return round((self.product.price - (self.product.price * self.product.discount/100) ) * self.quantity,2)
    @property
    def variant_sub_total(self):
        return round((self.variant.variant_price  - (self.variant.variant_price * self.variant.variant_discount/100)) * self.quantity,2)
        
    