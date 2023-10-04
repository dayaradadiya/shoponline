from datetime import datetime
import json
import math
import random
import string
import uuid
from django.db import models
from django.utils import timezone
import slugify
from accounts.models import User
from accounts.validators import file_size, validate_file_mimetype
from store.models import Product, Variants, Variation
from vendor.models import Vendor
from django.utils.timesince import timesince
from datetime import time
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from datetime import date, timedelta

request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal','PayPal'),
        ('Stripe','Stripe')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.payment_id
    
def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
     return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
     if new_slug is not None:
          slug = new_slug
     else :
          slug = slugify(instance.title)
     Klass= instance.__class__
     qs_exists = Klass.objects.filter(slug=slug).exists()  
     if qs_exists:   
          new_slug = "{slug}={randstr}".format(
              slug=slug,
              randstr=random_string_generator(size=4) 
          )
          return unique_slug_generator(instance, new_slug=new_slug)
     return slug

def unique_order_id_generator(instance):
     order_new_id = random_string_generator()
     Klass= instance.__class__
     qs_exists = Klass.objects.filter(order_number = order_new_id).exists()
     if qs_exists:
          return unique_slug_generator(instance)
     return order_new_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Packed', 'Packed'),
        ('ReadyToShip', 'ReadyToShip'),
        ('PickedUpToDeliver','PickedUpToDeliver'),
        ('Completed', 'Completed'),
        ('Delivered', 'Delivered'),
        ('Cancelled Order', 'Cancelled Order'),
        ('Return/Refund', 'Return/Refund'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor,blank=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=300)
    unit_no = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50,blank=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    total_weight = models.JSONField(blank=True, null=True)
    tax_data = models.JSONField(blank=True, null=True)
    tax = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=30)
    total_shipping_charge = models.FloatField(blank=True, null=True)
    total_quantity =  models.IntegerField()
    parcel_data = models.JSONField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(max_length=150,blank=True, null=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'
        

    def full_address(self):
        return f'{self.unit_no} {self.address_line_1}'

    def __str__(self):
        return self.order_number
    
    @property
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])
    
   
    def get_total_by_vendor(self):
        totaldata = {}
        subtotal = 0
        vendor = Vendor.objects.get(user=request_object.user)
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))
        return data
    
  
    def get_totalweight_by_vendor(self):
        totaldata = {}
        subtotal = 0
        vendor = Vendor.objects.get(user=request_object.user)
        if self.total_weight:
            total_weight = json.loads(self.total_weight)
            data = total_weight.get(str(vendor.id))
        return data
    
    @property
    def days_since_created(self):
        diff = timezone.now() - self.created_at
        return diff.days
    
def pre_save_create_order_number(sender,instance,*args,**kwargs):
     if not instance.order_number:
          instance.order_number = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_number,sender=Order)
 



class OrderProduct(models.Model):

    STATUS = (
        ('New', 'New'),
        ('Packed', 'Packed'),
        ('ReadyToShip', 'ReadyToShip'),
        ('PickedUpToDeliver','PickedUpToDeliver'),
        ('Completed', 'Completed'),
        ('Cancelled Item', 'Cancelled Item'),
        ('Cancelled Order', 'Cancelled Order'),
        ('Return/Refund', 'Return/Refund'),
        ('Return Requested','Return Requested')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    total_product_amt = models.FloatField(blank=True,null=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    is_delivered = models.BooleanField(default=False) 
    delivered_date = models.DateField(blank=True,null=True)
    completed_date = models.DateField(blank=True,null=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    cust_refund_for_cancelitem = models.FloatField(default=0)
    ref_code = models.CharField(max_length=30)
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    vendor = models.ForeignKey(Vendor,on_delete = models.SET_NULL,blank=True, null=True)
    SLA_Extension = models.IntegerField(blank=True, null=True)
    sla_ext_date = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.CharField(max_length=150,blank=True, null=True)


    def __str__(self):
        return self.product.product_name

    @property
    def sub_total(self):
        return round((self.product_price * self.quantity),2)
    
    def get_time_diff(self):
        ext_hrs = 0
        if self.SLA_Extension:
             if self.SLA_Extension == 1:
                ext_hrs = 24
             elif self.SLA_Extension == 2:
                 ext_hrs = 48
             else:
                 ext_hrs = 72
        dt1 = self.created_at.replace(tzinfo=None)
        dt2 = datetime.now().replace(tzinfo=None)
        # tdelta = dt2.astimezone() - dt1
        tdelta = dt2-dt1 
        tsecs = tdelta.total_seconds()
        # epochZero = datetime(2023,7,28,tzinfo = self.created_at.tzinfo)
        # return (self.created_at - epochZero).total_seconds()/(60*60)
        day = self.created_at.strftime('%A')
        if day in ['Friday', 'Saturday','Sunday']:
             return round((96 + ext_hrs - (tsecs/(60*60))),2)
        else :
            return round((72 + ext_hrs - (tsecs/(60*60))) ,2)
    def get_time_diff_readytoship(self):
        dt1 = self.updated_at.replace(tzinfo=None)
        dt2 = datetime.now().replace(tzinfo=None)
        # tdelta = dt2.astimezone() - dt1 
        tdelta = dt2 - dt1 
        tsecs = tdelta.total_seconds()
        # epochZero = datetime(2023,7,28,tzinfo = self.created_at.tzinfo)
        # return (self.created_at - epochZero).total_seconds()/(60*60)
        day = self.updated_at.strftime('%A')
        if day in ['Friday', 'Saturday']:
             return round(72 - (tsecs/(60*60)),2) 
        else :
            return round(48 - (tsecs/(60*60)),2) 
        

    
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=50,default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."




    
class Return_main_reason(models.Model):
    REASON_MAIN_CHOICES = (
                                ("I have received my items but there are issues","I have received my items but there are issues"),
                                ("I didn’t receive my items","I didn’t receive my items"),
        )
    
    mainreason =  models.CharField(max_length=100, choices=REASON_MAIN_CHOICES) 

    def __str__(self):
         return self.mainreason

class Return_reason(models.Model):
     main_reason =  models.ForeignKey(Return_main_reason, on_delete=models.CASCADE,blank=True, null=True)
     reason =  models.CharField(max_length=100,blank=True, null=True)
     
     def __str__(self):
         return self.reason
     
class Refund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,on_delete = models.SET_NULL,blank=True, null=True)
    orderproduct = models.ForeignKey(OrderProduct, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,blank=True, null=True)
    product_total_weight = models.IntegerField(default=0,blank=True, null=True)
    product_price = models.FloatField(default=0,blank=True, null=True)
    total_product_amount = models.FloatField(default=0,blank=True, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    email = models.EmailField()
    ref_code = models.CharField(max_length=30)
    main_reason = models.ForeignKey(Return_main_reason, on_delete=models.CASCADE,blank=True, null=True)
    reason = models.ForeignKey(Return_reason, on_delete=models.CASCADE,blank=True, null=True) 
    terms_accepted = models.BooleanField(default=False)
    return_pickup_date = models.DateField(blank=True, null=True)
    returnback_pickup_date = models.DateField(blank=True, null=True)
    return_status = models.CharField(max_length=60,blank=True, null=True)
    refund_title = models.CharField(max_length=200,blank=True, null=True)
    buyer_return_status = models.CharField(max_length=60,blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    seller_payment = models.FloatField(default=0,blank=True, null=True)
    buyer_payment = models.FloatField(default=0,blank=True, null=True)
    refund_status = models.CharField(max_length=30,blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    completed_date = models.DateTimeField(blank=True, null=True)
    partial_offer_amount = models.FloatField(blank=True, null=True)
    partial_offer_cnt = models.IntegerField(default=0,blank=True, null=True)
    counter_amount = models.FloatField(default=0,blank=True, null=True)
    returned_item_toseller = models.BooleanField(default=False)
    returned_item_tobuyer = models.BooleanField(default=False)
    transaction_fees = models.FloatField(blank=True, null=True)
    platform_fees = models.FloatField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.reason.reason}"

ext_validator = FileExtensionValidator(['jpg','png','jpeg'])  

class RefundImages(models.Model):
       refund = models.ForeignKey(Refund, on_delete=models.CASCADE)
       title = models.CharField(max_length=50,blank=True)
       image = models.FileField(upload_to='image/refund',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])

       def __str__(self):
              return self.title
       
       @property
       def image_tag_url(self):
                if self.image is not None:
                        return  mark_safe('<img src="{}" style="height:100px;"/>'.format(self.image.url))
                else:
                        return "" 
   
class ReturnDispute(models.Model):
       refund = models.ForeignKey(Refund, on_delete=models.CASCADE)
       dispute_reason = models.CharField(max_length=100,blank=True)
       description = models.CharField(max_length=500,blank=True)
       videofile = models.FileField(upload_to='dispute/videos',blank=True,null=True,validators=[file_size])
       videopod = models.FileField(upload_to='dispute/videos',blank=True,null=True,validators=[file_size])

       def __str__(self):
              return self.dispute_reason

class DisputeImages(models.Model):
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE)
    image =   models.FileField(upload_to='dispute/images',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
   

    def __str__(self):
              return self.refund
    


class VendorPayout(models.Model):
    PAYOUT_STATUS = (
        ('Refunded','Refunded'),
        ('Succeed','Succeed'),
        ('Pending','Pending')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE) ## done
    vendor =  models.ForeignKey(Vendor,on_delete = models.CASCADE, blank=True, null=True)  ## done
    week_duration = models.CharField(max_length=30)
    shipchargepaid_by_cust  = models.FloatField(default=0)
    shipcharge_to_seller = models.FloatField(default=0)
    amt_paid_by_customer = models.FloatField(default=0)
    completed_item_amt = models.FloatField(default=0) 
    cancelled_item_amt = models.FloatField(default=0) 
    processed_flag  = models.BooleanField(default=False)
    items_amount = models.FloatField(default=0)
    stripe_transaction_fees  = models.FloatField(default=0)
    platform_fees  = models.FloatField(default=0)
    total_vendor_payout  = models.FloatField(default=0)
    total_customer_payout  = models.FloatField(default=0)
    is_ordered = models.BooleanField(default=False)
    total_shipping_payout = models.FloatField(default=0)
    cust_refund_for_returnitem = models.FloatField(default=0)
    cancelled_item_data =  models.JSONField(blank=True, null=True)
    return_item_data =  models.JSONField(blank=True, null=True)
    cust_refund_for_cancelitem = models.FloatField(default=0)
    return_cust_ship_fees =  models.BooleanField(blank=True, null=True)
    payout_status = models.CharField(max_length=20, choices=PAYOUT_STATUS, default='New')
    exclude_seller_ship_platform_fees = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    updated_date = models.DateField(default=datetime.now)
    order_status = models.CharField(max_length=20, blank=True, null=True)
    process_flag = models.BooleanField(default=False)
    start_date  = models.DateField(blank=True, null=True)
    end_date  = models.DateField(blank=True, null=True)
    actual_shipping_cost  = models.FloatField(default=0)
    parcel_weight = models.FloatField(default=0)
    calc_shipcharge_cust = models.FloatField(default=0)
    calc_shipcharge_seller = models.FloatField(default=0)
    shipping_adjustment = models.FloatField(default=0)



class Return_VendorPayout(models.Model):
    PAYOUT_STATUS = (
        ('Paid','Paid'),
        ('Pending','Pending'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE) ## done
    vendor =  models.ForeignKey(Vendor,on_delete = models.CASCADE, blank=True, null=True)  ## done
    shipchargepaid_by_cust  = models.FloatField(default=0)
    shipcharge_to_seller  = models.FloatField(default=0)
    amt_paid_by_customer = models.FloatField(default=0)
    items_amount = models.FloatField(default=0)
    stripe_transaction_fees  = models.FloatField(default=0)
    platform_fees  = models.FloatField(default=0)
    is_ordered = models.BooleanField(default=False)
    buyer_payment_amt = models.FloatField(default=0)
    seller_payment_amt = models.FloatField(default=0)
    item_returned_back_toBuyer =  models.JSONField(blank=True, null=True)
    item_returned_toSeller = models.JSONField(blank=True, null=True)
    item_refund_without_return =  models.JSONField(blank=True, null=True)
    cancelled_item_data =  models.JSONField(blank=True, null=True)
    return_rejected_data =  models.JSONField(blank=True, null=True)
    payout_status = models.CharField(max_length=20, choices=PAYOUT_STATUS, default='New')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    updated_date = models.DateField(default=datetime.now)
    returned_status =models.JSONField(blank=True, null=True)
    order_status = models.CharField(max_length=20, blank=True, null=True)
    start_date  = models.DateField(blank=True, null=True)
    end_date  = models.DateField(blank=True, null=True)
    actual_shipping_cost  = models.FloatField(default=0)
    calc_shipcharge_cust = models.FloatField(default=0)
    calc_shipcharge_seller = models.FloatField(default=0)
    shipping_adjustment = models.FloatField(default=0)
    total_vendor_payout  = models.FloatField(default=0)
    total_customer_payout  = models.FloatField(default=0)
    total_shipping_payout = models.FloatField(default=0)
    return_exists = models.BooleanField(default=False)
    parcel_weight_toseller  =  models.JSONField(blank=True, null=True)
    parcel_weight_tobuyer  =  models.JSONField(blank=True, null=True)
    return_item_toseller_flag = models.BooleanField(default=False)
    return_item_tobuyer_flag = models.BooleanField(default=False)
    process_flag = models.BooleanField(default=False)
        
    def __str__(self):    
        return self.vendor.vendor_name
