from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import messages,auth
from django.views import View
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from cart.models import Cart, CartItem
from cart.views import _cart_id, sellprice
from customers.models import Address
from orders.forms import OrderForm
from customers.forms import AddressForm, RefundForm
from orders.models import Order, OrderProduct, OrderUpdate, Payment, Refund, Return_VendorPayout, VendorPayout
from orders.utils import generate_order_number, order_total_by_vendor, shipgcharge_c_to_v, totalcost_c_to_v
from shipping.models import ShipCharge, Shipping
from shoponline import settings
import json
from django.http import HttpResponse
from django.contrib import messages,auth
from django.template.loader import  render_to_string
from  django.contrib.auth.decorators import login_required,user_passes_test
from store.models import Product, Variants
import stripe
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta
from vendor.models import Vendor
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.sites.shortcuts import get_current_site
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Now

# Create your views here.

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k=20))


@login_required(login_url='login')
def payments(request):
      body = json.loads(request.body)
      order_number = body['orderID']
      order = Order.objects.get(user = request.user, order_number = order_number)
      VendorPayout.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now(),updated_date=Now())
      Return_VendorPayout.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now(),updated_date=Now())
      Shipping.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now())
      payment = Payment(
        user = request.user ,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
      payment.save()

      order.payment = payment
      order.is_ordered = True
      ref_code_temp = create_ref_code()
      order.ref_code = ref_code_temp
      order.status = 'New'
      order.save()
      update=OrderUpdate(order_id=order_number, update_desc="The order has been placed")
      update.save()

    # move the cart items to order products table
      cart_items = CartItem.objects.filter(user = request.user)
      
      for item in cart_items:
          orderproduct = OrderProduct()
          orderproduct.order_id = order.id   
          orderproduct.payment = payment
          orderproduct.user_id = request.user.id
          orderproduct.product_id = item.product_id
          orderproduct.quantity = item.quantity
          orderproduct.ref_code = ref_code_temp
          orderproduct.vendor = item.product.vendor
          if item.product.variant == 'None':
              orderproduct.product_price = sellprice(item.product.price,item.product.discount)
          else:
              orderproduct.product_price = sellprice(item.variant.variant_price,item.variant.variant_discount)
          orderproduct.variant_id = item.variant_id
          orderproduct.total_product_amt = round(orderproduct.product_price * orderproduct.quantity,2)
          orderproduct.ordered = True
          orderproduct.save()

        #   cart_item = CartItem.objects.get(id = item.id)
        #   product_variations = cart_item.variations.all()
        #   orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        #   orderproduct.variations.set(product_variations)
        #   orderproduct.save()

        #reduce the quantity of the sold product
          if item.product.variant == 'None':
               product = Product.objects.get(id = item.product_id )
               product.stock  -= item.quantity
               product.save()
          else:
               variant = Variants.objects.get(id = item.variant_id)
               variant.variant_stock  -= item.quantity
               variant.save()

    

    #send order received email to customer
      
      mail_subject = "Thank you for your order!"
      mail_template = "orders/order_confirmation_email.html"
      orders = Order.objects.get(order_number=order_number,is_ordered = True)
      ordered_product = OrderProduct.objects.filter(order=order)
      customer_subtotal=0
      for item in ordered_product:
           customer_subtotal += (item.product_price * item.quantity)
      customer_subtotal = round(customer_subtotal,2)
      context =  {
                  'user': request.user,
                  'order': orders,
                  'to_email' : order.email,
                  'trans_id' : body['transID'],
                  'ordered_product' : ordered_product,
                  'domain' : get_current_site(request),
                  'customer_subtotal' : customer_subtotal,
                  'shipping_charge' : orders.total_shipping_charge,
                  'grand_total' : orders.order_total
              }
      send_notification(mail_subject,mail_template,context)

      #send order received email to vendor
      mail_subject = "You have received a new order"
      mail_template = "orders/new_order_received.html"
      to_emails = []
      for i in cart_items :
            if i.product.vendor.user.email not in to_emails:
                to_emails.append(i.product.vendor.user.email)

            ordered_product_to_vendor = OrderProduct.objects.filter(order=order, product__vendor=i.product.vendor)

            context = {
                    'user' : request.user,
                    'order' : orders,
                    'trans_id' : body['transID'],
                    'to_email' : i.product.vendor.user.email,
                    'ordered_product_to_vendor' :ordered_product_to_vendor,
                    'vendor_subtotal' : order_total_by_vendor(orders,i.product.vendor.id),
                    'vendor_ship_charge' : shipgcharge_c_to_v(orders,i.product.vendor.id),
                    'vendor_total' : totalcost_c_to_v(orders,i.product.vendor.id),
                }
            send_notification(mail_subject,mail_template,context)

      #clear cart
      CartItem.objects.filter(user=request.user).delete()

      #send order number and transaction id back to sendData method via json response
      data = {
          'order_number' : order.order_number,
          'transaction_no' : payment.payment_id
      }
      return JsonResponse(data)

@login_required(login_url='login')
def place_order(request,total=0,quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
         render(request,'store')
    
    vendors_ids = []
    for i in cart_items:
         if i.product.vendor.id not in vendors_ids:
              vendors_ids.append(i.product.vendor.id)


         
    # parcel_str = ','.join(parcel_items)

    #caculate total data
    subtotal=0
    total_data={}
    for i in cart_items:
         product = Product.objects.get(pk=i.product.id,vendor_id__in=vendors_ids)
         v_id = product.vendor.id
         if v_id in total_data:
              subtotal = total_data[v_id]

              if i.product.variant == 'None':
                 subtotal += (sellprice(product.price,product.discount) * i.quantity)

                 
              else:
                subtotal += (sellprice(i.variant.variant_price,i.variant.variant_discount) * i.quantity)

              total_data[v_id] = round(subtotal,2)
         else:
              subtotal=0
              if i.product.variant == 'None':
                 subtotal += (sellprice(product.price,product.discount) * i.quantity)
                  
              else:
                subtotal +=  (sellprice(i.variant.variant_price,i.variant.variant_discount) * i.quantity)
               
              total_data[v_id] = round(subtotal,2)
    
    temp_total=0
    grand_total= 0
    total_quantity = 0
    tax=0
    for cart_item in cart_items:
            if cart_item.product.variant == 'None':
               temp_total += (sellprice(cart_item.product.price,cart_item.product.discount) * cart_item.quantity)
                 
            else:
                temp_total += (sellprice(cart_item.variant.variant_price,cart_item.variant.variant_discount) * cart_item.quantity)
             

            total = round(temp_total,2)
            quantity += cart_item.quantity
            total_quantity += cart_item.quantity

    

    # tax = total*0.08
    tax = total*0

    #caculate total weight for all vendors
    subweight=0
    total_weight={}
    for i in cart_items:
         product = Product.objects.get(pk=i.product.id,vendor_id__in=vendors_ids)
         v_id = product.vendor.id
         if v_id in total_weight:
                subweight = total_weight[v_id]
                subweight += (product.weight * i.quantity)
                total_weight[v_id] = subweight
         else:
              subweight=0
              subweight += (product.weight * i.quantity)
              total_weight[v_id] = subweight
    
    grand_total_temp = round(total + tax,2)
        

    if request.method == 'POST':
         form = AddressForm(request.POST)
         if form.is_valid():
                
                order = Order()
                order.user = current_user
                order.first_name = form.cleaned_data['first_name'] 
                order.last_name = form.cleaned_data['last_name'] 
                order.phone = form.cleaned_data['mobile']
                order.email = request.POST.get('email')
                order.address_line_1 = form.cleaned_data['address_line_1']
                order.unit_no = form.cleaned_data['unit_no']
                order.pin_code= form.cleaned_data['postal_code']
                order.country= form.cleaned_data['country']
                order.order_note= request.POST.get('order_note')
                order.order_total= grand_total_temp
                order.total_data = json.dumps(total_data)
                order.total_weight = json.dumps(total_weight)
                # order.parcel_data = json.dumps(parcel_data)
                order.tax= tax
                order.ip= request.META.get('REMOTE_ADDR')
                order.total_quantity = total_quantity
                order.save()

                # order_number = generate_order_number(order.id)
                # order.order_number = order_number
                order.vendors.add(*vendors_ids)
                order.save()
                
                address = Address.objects.filter(user=request.user)
                if address.count() < 1 :
                    address = Address()
                    address.user=request.user
                    address.first_name = order.first_name
                    address.last_name = order.last_name
                    address.mobile = order.phone
                    address.address_line_1 = order.address_line_1
                    address.unit_no  = order.unit_no
                    address.status = True
                    address.country = order.country
                    address.postal_code = order.pin_code
                    address.save()
                else :
                    address = Address.objects.get(user=request.user, status=True)
                    address.user=request.user
                    address.first_name = order.first_name
                    address.last_name = order.last_name
                    address.mobile = order.phone
                    address.address_line_1 = order.address_line_1
                    address.unit_no  = order.unit_no
                    address.status = True
                    address.country = order.country
                    address.postal_code = order.pin_code
                    address.save()

                pub_key = settings.STRIPE_PUBLISHABLE_KEY
                order = Order.objects.get(user=current_user, is_ordered=False, id=order.id)
                
                #chipping details
                
                
            	
                #calculate shipping charge
                total_ship_charge = 0
                weight_by_vendor = 0
                ship_charge_cust = 0
                ship_charge_seller = 0
                for v_id in total_weight:
                    if order.total_weight:
                        total_weight = json.loads(order.total_weight)
                        weight_by_vendor =  total_weight.get(str(v_id))
                        print('weight_by_vendor is :',weight_by_vendor)
                        ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=weight_by_vendor,max_weight_limit__gte=weight_by_vendor)
                        ship_charge_cust = ship_cost.buyer_shipping_fees
                        ship_charge_seller = ship_cost.seller_shipping_fees

                        # calculate if shipping charge is exempted?     
                        if v_id in vendors_ids:
                            vendor = Vendor.objects.get(id=v_id)
                            total_data = json.loads(order.total_data)
                            total_amount =  total_data.get(str(v_id))
                            if total_amount >= vendor.free_del_amount_limit:
                                ship_charge_cust = 0
                                ship_charge_seller = ship_cost.buyer_shipping_fees + ship_cost.seller_shipping_fees

                            #shipping information
                            shipping= Shipping()
                            shipping.order_id = order.id     
                            shipping.vendor_id = v_id	
                            shipping.receiver_name = order.first_name + order.last_name 				
                            shipping.receiver_contact =	order.phone		
                            shipping.receiver_email	= order.email 	
                            shipping.receiver_unit = order.unit_no 		
                            shipping.receiver_postcode = order.pin_code	
                            shipping.sender_name =	vendor.vendor_name
                            if 	vendor.stype == 1:
                               if vendor.user.icprofile :	
                                    shipping.sender_company = vendor.user.icprofile.full_name_ic	
                            else:
                                if vendor.user.businessprofile :
                                     shipping.sender_company = vendor.user.businessprofile.company_name			
                            shipping.sender_contact = vendor.user.phone_number	
                            shipping.sender_alt_contact =vendor.user.userprofile.alt_phone_number	
                            shipping.sender_email =	vendor.user.email	
                            shipping.sender_unit = vendor.user.userprofile.unit_no
                            shipping.sender_postcode =vendor.user.userprofile.pin_code
                            shipping.save()

                            vendorpayout = VendorPayout()
                            vendorpayout.order_id = order.id     
                            vendorpayout.vendor_id = v_id
                            vendorpayout.shipchargepaid_by_cust = ship_charge_cust
                            vendorpayout.shipcharge_to_seller = ship_charge_seller
                            vendorpayout.amt_paid_by_customer = (total_amount + ship_charge_cust)
                            vendorpayout.items_amount = total_amount
                        
                            vendorpayout.actual_shipping_cost = ship_cost.currier_service_ship_fees
                            
                            today = date.today()
                            start = today - timedelta(days=today.weekday())
                            end = start + timedelta(days=6)
                            vendorpayout.start_date = start
                            vendorpayout.end_date = end
                            vendorpayout.save()


                            return_vendorpayout = Return_VendorPayout()
                            return_vendorpayout.order_id = order.id     
                            return_vendorpayout.vendor_id = v_id
                            return_vendorpayout.shipchargepaid_by_cust = ship_charge_cust
                            return_vendorpayout.shipcharge_to_seller = ship_charge_seller
                            return_vendorpayout.amt_paid_by_customer = (total_amount + ship_charge_cust)
                            return_vendorpayout.items_amount = total_amount
                        
                            return_vendorpayout.actual_shipping_cost = ship_cost.currier_service_ship_fees
                            return_vendorpayout.start_date = start
                            return_vendorpayout.end_date = end
                            return_vendorpayout.save()
                            
                        total_ship_charge += ship_charge_cust

                grand_total = round(grand_total_temp + total_ship_charge,2)

                order.order_total = grand_total
                order.total_shipping_charge = total_ship_charge
                order.save()
                vendor_p = VendorPayout.objects.filter(order_id = order.id)
                vendor_p_cnt = vendor_p.count()

                today = date.today()
                start = today + timedelta(days=3)
                end = start + timedelta(days=4)
                startdate =  start.strftime("%d-%b")
                enddate = end.strftime("%d-%b")

                context={
                    'order':order,
                    'cart_items' : cart_items,
                    'tax' : tax,
                    'grand_total' : grand_total,
                    'total' : total,
                    'pub_key':pub_key,
                    'total_ship_charge' : total_ship_charge,
                    'vendor_p':vendor_p,
                    'startdate' : startdate,
                    'enddate' : enddate,
                    'vendor_p_cnt':vendor_p_cnt,
                 }
                return render(request,'orders/payments.html',context)
         else:
                print(form.errors)
                return redirect('checkout')

@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    temp_subtotal = 0
    try:
        order = Order.objects.get(order_number=order_number,is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id=transID)

        subtotal = 0
        for i in ordered_products:
            
             temp_subtotal += (i.product_price * i.quantity)
            
             subtotal = round(temp_subtotal,2)

        context = {
            'order' : order,
            'ordered_products' : ordered_products,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal' : subtotal,
        }
        return render(request,'orders/order_complete.html',context)
    except (Payment.DoesNotExist , Order.DoesNotExist):
        return redirect('home')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        temp_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            address = Address.objects.filter(user=request.user)
            try:
                active_address = Address.objects.get(user=request.user,status=True)
            except:
                 messages.warning(request, "Add/Edit your default shipping ddress.")
                 if request.user.role == 'Vendor':
                      return redirect('vendor_address')
                 elif request.user.role == 'Customer':
                      return redirect('customer_address')
                 active_address = None
            user_profile = UserProfile.objects.get(user=request.user)
            # default_values = {
            #         'first_name' :request.user.first_name  ,
            #         'last_name' :request.user.last_name ,
            #         'phone' :active_address.mobile ,
            #         'email' :request.user.email ,
            #         'address_line_1' :active_address.address ,
            #         # 'country'   :user_profile.country ,
            #         # 'state' :user_profile.state ,
            #         # 'city' :user_profile.city ,
            #         'pin_code' :active_address.postal_code ,
            # }
            # form = OrderForm(initial=default_values)
           
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
            # form = None
        for cart_item in cart_items:
            price = 0
            discount = 0
            if cart_item.variant :
                price = cart_item.variant.variant_price
                discount = cart_item.variant.variant_discount
                temp_total += (sellprice(price,discount) * cart_item.quantity)
            else:
                price = cart_item.product.price
                discount = cart_item.product.discount
                temp_total += (sellprice(price,discount) * cart_item.quantity)
            total = round(temp_total,2)
            quantity += cart_item.quantity
        tax = (0*total)/100
        grand_total = round(tax + total,2)
        if active_address :
            form = AddressForm(instance=active_address)
        else:
             form = AddressForm()
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' :  cart_items,
        'grand_total' : grand_total,
        'tax' : tax,
        'active_address' : active_address,
        'user_profile' : user_profile,
        'form' : form,
        'address' : address,
    }

    return render(request,'orders/checkout.html',context)

def tracker2(request):
     if request.method == 'POST':
           orderNo = request.POST.get('orderID','')
           try:   
                order = Order.objects.filter(order_number=orderNo,is_ordered=True)
                if len(order)>0:
                        update = OrderUpdate.objects.filter(order_id = orderNo)
                        updates=[]
                        for item in update:
                            updates.append({'text':item.update_desc,'time':item.timestamp})
                            response = json.dumps(updates,default=str)
                        return HttpResponse(response)
                else:
                        return HttpResponse('{}')
           except Exception as e:
            return HttpResponse('{}')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email')
        try:
            order = Order.objects.filter(order_number=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse(f'exception {e}')

    return render(request, 'orders/tracker.html')



def order_complete_card(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user).order_by('created_at')
        order_number = request.GET.get('order_number')
        order = Order.objects.get(order_number=order_number,user=request.user)
        VendorPayout.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now(),updated_date=Now())
        Shipping.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now())
        Return_VendorPayout.objects.filter(order__order_number = order_number).update(is_ordered = True,updated_at=Now())
        
        ref_code_temp = create_ref_code()
        order.ref_code = ref_code_temp

        order.is_ordered = True
        order.status = 'New'
        order.save()


        #MOVE THE CART ITEMS TO ORDERED FOOD MODEL
        cart_items = CartItem.objects.filter(user=request.user)
        orderedproduct = OrderProduct()
        for item in cart_items:
                orderedproduct = OrderProduct()
                orderedproduct.order_id = order.id
                orderedproduct.payment = order.payment
                orderedproduct.user_id = request.user.id
                orderedproduct.product_id = item.product_id
                orderedproduct.quantity = item.quantity
                orderedproduct.ref_code = ref_code_temp
                orderedproduct.vendor = item.product.vendor
                if item.product.variant == 'None':
                  orderedproduct.product_price = sellprice(item.product.price,item.product.discount)
                else:
                    orderedproduct.product_price = sellprice(item.variant.variant_price,item.variant.variant_discount)
                orderedproduct.variant_id = item.variant_id
                orderedproduct.total_product_amt = round(orderedproduct.product_price * orderedproduct.quantity,2)
                orderedproduct.ordered = True
                orderedproduct.save()

            #reduce the quantity of the sold product
                if item.product.variant == 'None':
                    product = Product.objects.get(id = item.product_id )
                    product.stock  -= item.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id = item.variant_id)
                    variant.variant_stock  -= item.quantity
                    variant.save()
            

        #SEND EMAIL CONFIRMATION TO THE CUSTOMER
        ordered_product = OrderProduct.objects.filter(order_id=order.id)
        mail_subject="Thank you for ordering with us"
        mail_template = 'orders/order_confirmation_email.html'
            
        customer_subtotal = 0
        for item in ordered_product:
                customer_subtotal += (item.quantity * item.product_price)
        customer_subtotal = round(customer_subtotal,2)
            
        context={
                'user' : request.user,
                'order' : order,
                'to_email' : order.email,
                'ordered_product' : ordered_product,
                'domain': get_current_site(request),
                'customer_subtotal' : customer_subtotal,
                'shipping_charge' : order.total_shipping_charge,
                'grand_total' : order.order_total
            }
        send_notification(mail_subject,mail_template,context)
            
        #SEND ORDER RECEIVED EMAIL TO VENDOR
        mail_subject = "You have received a new order"
        mail_template = "orders/new_order_received.html"
        to_emails=[]
        for i in cart_items :
                if i.product.vendor.user.email not in to_emails:
                    to_emails.append(i.product.vendor.user.email)

                ordered_product_to_vendor = OrderProduct.objects.filter(order=order,product__vendor=i.product.vendor)                                                                                                                                                                                              
                context = {
                        'user' : request.user,
                        'order' : order,
                        'to_email' : i.product.vendor.user.email,
                        'ordered_product_to_vendor' : ordered_product_to_vendor,
                        'vendor_subtotal' : order_total_by_vendor(order,i.product.vendor.id),
                        'vendor_ship_charge' : shipgcharge_c_to_v(order,i.product.vendor.id),
                        'vendor_total' : totalcost_c_to_v(order,i.product.vendor.id),
                    }
                send_notification(mail_subject,mail_template,context)
        
        #clear cart
        CartItem.objects.filter(user=request.user).delete()
    except Exception as e:
        print(f'exception occured,{e} ')
   
    #Main functionality to send out emails to customer and vendor and populate invoice
    try:
        order = Order.objects.get(order_number=order_number,is_ordered = True,user=request.user)
        ordered_product = OrderProduct.objects.filter(order=order)
        subtotal = 0
        temp_subtotal = 0
        for i in ordered_product:
            
             temp_subtotal += (i.product_price * i.quantity)
            
             subtotal = round(temp_subtotal,2)
        context = {
            'order' : order,
            'ordered_product' : ordered_product, 
            'subtotal' : subtotal,
        }
        return render(request,'orders/order_complete_card.html',context)
    except Exception as e:
        print(f'exception occured,{e} ')
        return redirect('home')

def start_order(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('created_at')
    data=json.loads(request.body)
    order_number = data['order_number']
    order = Order.objects.get(order_number = order_number)
    items=[]
    for item in cart_items:
        total_price=0
        temp_total=0
        quantity = 0
        if item.variant :
                temp_total = sellprice(item.variant.variant_price,item.variant.variant_discount)
        else:
                temp_total  = sellprice(item.product.price ,item.product.discount)
        total_price = int(round(temp_total,2)*100)
        # total_price = "{0:.2f}".format(temp_total)
        quantity += item.quantity
        
        obj = {
            'price_data' :{
                'currency' : 'SGD',
                'product_data' : {
                    'name' : item.product.product_name,
                    # 'images' : ['https://i.image.com/123.png'],
                                 },
                'unit_amount' : total_price,
                          },
            'quantity' : item.quantity,
            }
        items.append(obj) 

    shipping_charge = int(round(order.total_shipping_charge,2)*100)
    ship_opt=[
    {
      "shipping_rate_data": {
        "type": "fixed_amount",
        "fixed_amount": {"amount": shipping_charge, "currency": "SGD"},
        "display_name": "Shipping Charges",
        "delivery_estimate": {
          "minimum": {"unit": "business_day", "value": 5},
          "maximum": {"unit": "business_day", "value": 7},
        },
      },
    },
   ]
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order_number = data['order_number']
    success_url = "http://127.0.0.1:8000/orders/order_complete_card/?order_number="+order_number
    cancel_url = "http://127.0.0.1:8000/orders/failed/"
    session = stripe.checkout.Session.create(
            shipping_options = ship_opt,
            payment_method_types = ['card'],
            line_items = items,
            mode = 'payment',
            success_url = success_url,
            cancel_url = cancel_url,
        )   
    payment_intent = session.payment_intent
    

    # modified to update payments in case of card payment

    
    transaction_id = session.id
    payment_method = 'card'
    status = 'Success'

    order =Order.objects.get(user=request.user,order_number=order_number)
    payment = Payment(
            user = request.user,
            payment_id = transaction_id,
            payment_method = payment_method,
            amount_paid = order.order_total,
            status = status
        )

    #UPDATE THE payment MODEL
    payment.save()

    #UPDATE THE order MODEL
    order.payment = payment
    
    ref_code_temp = create_ref_code()
    order.ref_code = ref_code_temp
    
    order.save()

    
            
    return JsonResponse({'session' : session,'order' : payment_intent})  

def success(request):
        return render(request,'orders/success.html')

def failed(request):
        return render(request,'orders/failed.html')

@login_required(login_url='login')
def edit_order_address(request,pk):
    if request.user.is_authenticated :
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address_line_1 = request.POST.get("address_line_1")
        unit_no = request.POST.get("unit_no")
        postal_code = request.POST.get("postal_code")
        mobile = request.POST.get("mobile")
        country = request.POST.get("country")

        if len(mobile) > 8  :
            messages.error(request, 'Mobile no should be 8 digit long')
            return redirect('checkout')
        elif  first_name == '' or last_name == '' or address_line_1 == '' or unit_no == '' or  postal_code == '' or country == '' :
             messages.error(request, 'Please fill all address details')
             return redirect('checkout')
        
        Address.objects.filter(user=request.user,pk=pk).update(user=request.user,
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            unit_no=unit_no,
            postal_code=postal_code,
            mobile=mobile,
            country=country)
    return redirect('checkout')

@login_required(login_url='login')
def delete_order_address(request,pk):
    if request.user.is_authenticated :
        address = get_object_or_404(Address, pk=pk)
        address.delete()
        messages.success(request,'Address has been deleted successfully!')
    return redirect('checkout')

# Using Django

@login_required(login_url='login')
def add_order_address(request):

    if request.user.is_authenticated :
        address = Address.objects.filter(user=request.user)

        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address_line_1 = request.POST.get("address_line_1")
            unit_no = request.POST.get("unit_no")
            postal_code = request.POST.get("postal_code")
            mobile = request.POST.get("mobile")
            country = request.POST.get("country")

            Address.objects.create(user=request.user,
                                                first_name=first_name, 
                                                last_name=last_name,
                                                address_line_1=address_line_1,
                                                unit_no=unit_no,
                                                postal_code=postal_code,
                                                country=country,
                                                mobile=mobile)
            messages.success(request,'Address added successfully.')
    return redirect("checkout")

@csrf_exempt
def my_webhook_backup(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret='whsec_57ce90f10b83093cb576c8c640c3e87ef9437547c269285e8abea2fa760b755d'

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f' valueerror exception occured,{e} ')
        return HttpResponse(status=400)
        
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f' SignatureVerificationError exception occured,{e} ')
        return HttpResponse(status=400)
    try:
        if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
            session = stripe.checkout.Session.retrieve(
            event['data']['object'],
            expand=['line_items'],
            )

    except Exception as e:
           print(f'exception occured,{e} ')
    # line_items = session.line_items
    # Fulfill the purchase...
    # fulfill_order(line_items)

    # Passed signature verification
    return HttpResponse(status=200)