
from django.db import models
from datetime import datetime
from orders.models import Order
from store.models import Product
from vendor.models import Vendor

# Create your models here.

class Shipping(models.Model):
    #shipping related data
    order = models.ForeignKey(Order, on_delete=models.CASCADE) ## done
    vendor =  models.ForeignKey(Vendor,on_delete = models.CASCADE, blank=True, null=True)  ## done
    parcel_content = models.CharField(max_length=200, blank=True, null=True) ##done
    parcel_value = models.FloatField(default=0, blank=True, null=True) ##done
    weight_kg = models.CharField(max_length=100, blank=True, null=True) ##done
    pickup_date = models.DateField(blank=True, null=True)
    sender_name = models.CharField(max_length=100, blank=True, null=True)  #### start done
    sender_company = models.CharField(max_length=100, blank=True, null=True)
    sender_contact = models.CharField(max_length=100, blank=True, null=True)
    sender_alt_contact = models.CharField(max_length=100, blank=True, null=True)
    sender_email = models.CharField(max_length=100, blank=True, null=True)
    sender_unit = models.CharField(max_length=100, blank=True, null=True)
    sender_postcode = models.CharField(max_length=100, blank=True, null=True)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_company = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact = models.CharField(max_length=100, blank=True, null=True)
    receiver_alt_contact = models.CharField(max_length=100, blank=True, null=True)
    receiver_email = models.CharField(max_length=100, blank=True, null=True)
    receiver_unit = models.CharField(max_length=100, blank=True, null=True)
    receiver_postcode = models.CharField(max_length=100, blank=True, null=True)
    courier_company = models.CharField(max_length=100, blank=True, null=True)
    alternative_courier_company = models.CharField(max_length=100, blank=True, null=True)
    sms = models.BooleanField(default=False,blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    amt_paid_by_customer = models.FloatField(default=0, blank=True, null=True)
    items_amount = models.FloatField(default=0, blank=True, null=True)
    shipchargepaid_by_cust = models.FloatField(default=0, blank=True, null=True)
    shipchargepaid_by_vendor = models.FloatField(default=0, blank=True, null=True) #### end done
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    is_ordered = models.BooleanField(default=False)

class Return_Shipping(models.Model):
    #shipping related data
    order = models.ForeignKey(Order, on_delete=models.CASCADE) ## done
    vendor =  models.ForeignKey(Vendor,on_delete = models.CASCADE, blank=True, null=True)  ## done
    parcel_content = models.CharField(max_length=200, blank=True, null=True) ##done
    parcel_value = models.FloatField(default=0, blank=True, null=True) ##done
    weight_kg = models.CharField(max_length=100, blank=True, null=True) ##done
    return_pickup_date = models.DateField(blank=True, null=True)
    returnback_pickup_date = models.DateField(blank=True, null=True)
    sender_name = models.CharField(max_length=100, blank=True, null=True)  #### start done
    sender_company = models.CharField(max_length=100, blank=True, null=True)
    sender_contact = models.CharField(max_length=100, blank=True, null=True)
    sender_alt_contact = models.CharField(max_length=100, blank=True, null=True)
    sender_email = models.CharField(max_length=100, blank=True, null=True)
    sender_unit = models.CharField(max_length=100, blank=True, null=True)
    sender_postcode = models.CharField(max_length=100, blank=True, null=True)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_company = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact = models.CharField(max_length=100, blank=True, null=True)
    receiver_alt_contact = models.CharField(max_length=100, blank=True, null=True)
    receiver_email = models.CharField(max_length=100, blank=True, null=True)
    receiver_unit = models.CharField(max_length=100, blank=True, null=True)
    receiver_postcode = models.CharField(max_length=100, blank=True, null=True)
    courier_company = models.CharField(max_length=100, blank=True, null=True)
    alternative_courier_company = models.CharField(max_length=100, blank=True, null=True)
    sms = models.BooleanField(default=False,blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    amt_paid_by_customer = models.FloatField(default=0, blank=True, null=True)
    items_amount = models.FloatField(default=0, blank=True, null=True)
    shipchargepaid_by_cust = models.FloatField(default=0, blank=True, null=True)
    shipchargepaid_by_vendor = models.FloatField(default=0, blank=True, null=True) #### end done
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    is_ordered = models.BooleanField(default=False)


class ShipCharge(models.Model):
    currier_type = models.CharField(max_length=100, blank=True, null=True)
    min_weight_limit = models.IntegerField(default=0, blank=True, null=True)
    max_weight_limit = models.IntegerField(default=0, blank=True, null=True)
    buyer_shipping_fees =  models.FloatField(default=0, blank=True, null=True)
    seller_shipping_fees =  models.FloatField(default=0, blank=True, null=True)
    currier_service_ship_fees =  models.FloatField(default=0, blank=True, null=True)