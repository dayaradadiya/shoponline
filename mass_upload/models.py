from django.db import models
from ckeditor.fields import RichTextField
from store.models import Product, Variants
from vendor.models import Vendor

# Create your models here.

status_choice = (
       ('Successful','Successful'),
       ('Unsuccessful','Unsuccessful'),
       ('Partially Successful','Partially Successful'),
       ('Upload Failed','Upload Failed')
)

# record level status
class StgProduct(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    category_id = models.CharField(max_length=1000,null=True,blank=True)
    product_name = models.CharField(max_length=1000,null=True,blank=True)
    featured_image= models.CharField(max_length=1000,null=True,blank=True)
    image1 = models.CharField(max_length=1000,null=True,blank=True)
    image2= models.CharField(max_length=1000,null=True,blank=True)
    image3= models.CharField(max_length=1000,null=True,blank=True)
    image4= models.CharField(max_length=1000,null=True,blank=True)
    image5= models.CharField(max_length=1000,null=True,blank=True)
    image6= models.CharField(max_length=1000,null=True,blank=True)
    image7= models.CharField(max_length=1000,null=True,blank=True)
    image8= models.CharField(max_length=1000,null=True,blank=True)
    brand = models.CharField(max_length=1000,null=True,blank=True)
    product_information = models.TextField(null=True,blank=True)
    variant = models.CharField(max_length=1000,null=True,blank=True)
    variant_title= models.CharField(max_length=1000,null=True,blank=True)
    variant_color = models.CharField(max_length=1000,null=True,blank=True)
    variant_size = models.CharField(max_length=1000,null=True,blank=True)
    image_variant = models.CharField(max_length=1000,null=True,blank=True)
    variant_stock = models.CharField(max_length=1000,null=True,blank=True)
    variant_price = models.CharField(max_length=1000,null=True,blank=True)
    variant_discount = models.CharField(max_length=1000,null=True,blank=True)
    variant_max_allowed_quantity = models.CharField(max_length=1000,null=True,blank=True)
    stock = models.CharField(max_length=1000,null=True,blank=True)
    price = models.CharField(max_length=1000,null=True,blank=True)
    discount = models.CharField(max_length=1000,null=True,blank=True)
    weight = models.CharField(max_length=1000,null=True,blank=True)
    parcel_size_L = models.CharField(max_length=1000,null=True,blank=True)
    parcel_size_W = models.CharField(max_length=1000,null=True,blank=True)
    parcel_size_H = models.CharField(max_length=1000,null=True,blank=True)
    max_allowed_quantity = models.CharField(max_length=1000,null=True,blank=True)
    min_order_quantity = models.CharField(max_length=1000,null=True,blank=True)
    file_name = models.CharField(max_length=1000,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    status = models.CharField(max_length=1000,null=True,blank=True)
    error =  models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):  
                return self.status

     

class ProductRecord(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    file_name =  models.CharField(max_length=100,null=True,blank=True)
    processed = models.IntegerField(default=0, null=True,blank=True)
    products = models.IntegerField(default=0, null=True,blank=True)
    status = models.CharField(max_length=100,choices=status_choice)

    def __str__(self):  
                return self.status
    
def sku(last_sku):
    sku = last_sku[:4]
    sku += str(int(last_sku[4:]) + 1).zfill(4)
    return sku
    
class Stock_keeping_unit(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    product =  models.ForeignKey(Product,on_delete = models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete = models.CASCADE,blank=True,null=True)
   

    # def save(self, *args, **kwargs):
    #     if not self.sku:
    #         product_id = self.product.id
    #         try:
    #             last = Stock_keeping_unit.objects.filter(product_id = product_id).latest('sku')
    #             self.sku = sku(last.sku)
    #         except Stock_keeping_unit.DoesNotExist:
    #             self.sku = self.product_id + int('0001')
    #     super(Stock_keeping_unit,self).save(*args,**kwargs)




