from django.contrib import admin


from .models import ShipCharge, Shipping

# Register your models here.

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order','vendor','parcel_content','parcel_value','pickup_date','sender_name','receiver_name','courier_company','alternative_courier_company','sms','reference','amt_paid_by_customer','items_amount','shipchargepaid_by_cust')
    list_filter = ['order','vendor','parcel_content','parcel_value','pickup_date','sender_name','receiver_name','courier_company','alternative_courier_company','sms','reference','amt_paid_by_customer','items_amount','shipchargepaid_by_cust']
    readonly_fields = ('order','vendor','parcel_content','parcel_value','pickup_date','sender_name','receiver_name','courier_company','alternative_courier_company','sms','reference','amt_paid_by_customer','items_amount','shipchargepaid_by_cust')
 
class ShipChargeAdmin(admin.ModelAdmin):
    list_display = ('currier_type','min_weight_limit', 'max_weight_limit', 'buyer_shipping_fees' ,'seller_shipping_fees' )
    list_filter = ['currier_type','min_weight_limit', 'max_weight_limit', 'buyer_shipping_fees' ,'seller_shipping_fees' ]
    readony_fields = ('currier_type','min_weight_limit', 'max_weight_limit', 'buyer_shipping_fees' ,'seller_shipping_fees' )
    


admin.site.register(Shipping,ShippingAdmin)
admin.site.register(ShipCharge,ShipChargeAdmin)

