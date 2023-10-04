
import datetime
import json

from shipping.models import Shipping
def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_datetime + str(pk)
    return order_number

def order_total_by_vendor(orders,vendor_id):
    total_data = json.loads(orders.total_data)
    data = total_data.get(str(vendor_id))
    return data

def shipgcharge_c_to_v(order,vendor_id):
    shipg = Shipping.objects.get(order=order,vendor_id=vendor_id,is_ordered=True)
    return shipg.shipchargepaid_by_cust

def totalcost_c_to_v(order,vendor_id):
   shipg = Shipping.objects.get(order=order,vendor_id=vendor_id,is_ordered=True)
   return shipg.amt_paid_by_customer

