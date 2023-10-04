import json
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.utils.timezone import datetime
from accounts.models import User
from accounts.views import admin_check, is_admin
from cart.views import sellprice
from customadmin import admin
from customadmin.models import Mappings
from orders.models import Order, OrderProduct, Refund, Return_VendorPayout, VendorPayout
from shipping.models import Return_Shipping, ShipCharge, Shipping
from store.models import Product
from django.db.models import Q
from django.utils import timezone

# Create your views here.
from django.db.models.functions import ExtractYear, ExtractWeek
from django.db.models import Sum,Count
from django.db.models import F
from datetime import date, timedelta
from  django.contrib.auth.decorators import login_required
from django.db.models.functions import Now
from django.core.paginator import Paginator
from  django.contrib.auth.decorators import login_required,user_passes_test

from vendor.models import Vendor

def admin_login(request):
    try:
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in!')
            return redirect('dashboard')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            
            if user.is_superadmin:
                    login(request, user)
                    return redirect('/admin/dashboard/')
            messages.error(request,'Invalid login credentials')
            return redirect('/')
        return render(request,'admin/login.html')
    
    except Exception as e:
             print(e)

@user_passes_test(is_admin)
def dashboard(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]

    context={
        'orders' : orders,
        'recent_orders' : recent_orders,

    }
    return render(request,'admin/dashboard.html',context)

@user_passes_test(is_admin)
def generateShipping(request):
    
    orders = Order.objects.filter(status="ReadyToShip",is_ordered=True)

    for order in orders :
        vendors_ids = []
        orderproducts = OrderProduct.objects.filter(order_id = order.id,status="ReadyToShip",)
        for i in orderproducts:
            if i.product.vendor.id not in vendors_ids:
                vendors_ids.append(i.product.vendor.id)
        #get parcel items for shipping
        parcel_data={}
        parcel_str = ''
        for i in orderproducts:
            product = Product.objects.get(pk=i.product.id,vendor_id__in=vendors_ids)
            v_id = product.vendor.id
            if v_id in parcel_data:
                parcel_str = parcel_data[v_id]
                parcel_str = product.product_name[:30] + ','+ parcel_str
                parcel_data[v_id] = parcel_str
            else:
                parcel_str=''
                parcel_str = product.product_name[:30] + ','+ parcel_str 
                parcel_data[v_id] = parcel_str

        
        
        subweight=0
        total_weight={}
        for i in orderproducts:
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
        
        

        subtotal=0
        total_data={}
        
        for i in orderproducts:
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

        for v_id in vendors_ids:
            shipping =  Shipping.objects.get(order_id=order.id,vendor_id=v_id,is_ordered=True)
            shipping.parcel_content = parcel_data[v_id]
            shipping.weight_kg =  (total_weight[v_id]/1000)
            shipping.parcel_value =  total_data[v_id]  
            shipping.save()
    today = timezone.now().date()
               
    # ship_details = Shipping.objects.filter(Q(updated_at__date=today) |
    #                 Q(updated_at__date=today),is_ordered=True)
    
    ship_details = Shipping.objects.filter(is_ordered=True)   
    
    context={
         'ship_details' : ship_details
    }
             
    return render(request,'admin/generate.html',context)





@user_passes_test(is_admin)
def return_process(request):
    all_refund = Refund.objects.all().order_by('-created_at')
    dispute_cases = Refund.objects.filter(return_status__in=["Evidence Submitted","Reject Evidence Submitted"]).order_by('-updated_at')

    return_notdelivered_cases = Refund.objects.filter(return_status="Return Not Delivered").order_by('-updated_at')
    
    return_readytoship_cases = Refund.objects.filter(return_status__in = ["Return ReadyToShip","Return Back ReadyToShip"]).order_by('-updated_at')

    readytoprocess_cases = Refund.objects.filter(return_status="ReadyToProcess").order_by('-updated_at')

    return_requestcancelled = Refund.objects.filter(return_status="Return Request Cancelled").order_by('-updated_at')

    paginator = Paginator(all_refund,10)
    page_all = request.GET.get('page')
    page_refund_all = paginator.get_page(page_all)
    
    # tohsip
    paginator = Paginator(dispute_cases,10)
    page_dispute= request.GET.get('page')
    page_dispute_cases = paginator.get_page(page_dispute)


    paginator = Paginator(return_notdelivered_cases,10)
    page_notdelivered= request.GET.get('page')
    page_notdelivered_cases = paginator.get_page(page_notdelivered)

    paginator = Paginator(return_readytoship_cases,10)
    page_readytoship= request.GET.get('page')
    page_readytoship_cases = paginator.get_page(page_readytoship)

    paginator = Paginator(readytoprocess_cases,10)
    page_readytoprocess= request.GET.get('page')
    page_readytoprocess_cases = paginator.get_page(page_readytoprocess)

    paginator = Paginator(return_requestcancelled,10)
    page_cancelled= request.GET.get('page')
    page_requestcancelled = paginator.get_page(page_cancelled)


    context={
        'all_refund' : page_refund_all,
        'dispute_cases' : page_dispute_cases,
        'return_notdelivered_cases' : page_notdelivered_cases,
        'return_readytoship_cases' : page_readytoship_cases,
        'readytoprocess_cases': page_readytoprocess_cases,
        'return_requestcancelled' : page_requestcancelled,
    } 
    return render(request,'admin/return_refund.html',context)

@user_passes_test(is_admin)
def shop_approval(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    try:
        if request.method == "POST":
            if refund.return_status == 'Reject Evidence Submitted':
                    refund.return_status='Dispute Approved'
                    refund.refund_title = 'Buyer will not refunded, refund request will be rejected'
                    refund.buyer_return_status='Request Rejected'

            elif refund.return_status == 'Evidence Submitted':
                    refund.return_status = 'Return Back To Buyer'
                    refund.refund_title = 'Buyer will not refunded, Seller will send item back to Buyer'
                    orderproduct.status = 'Return Back To Buyer'
                    refund.buyer_return_status='Return Rejected'
                    
            refund.seller_payment = refund.total_product_amount
            refund.buyer_payment = 0
            refund.completed_date = Now()
            refund.updated_at = Now()
            refund.save()

            
           
           
            messages.success(request, "Seller dispute is approved")
    except Exception as e:
         print(f'exception occured,{e}')
         messages.error(request, "exception raised")
    return redirect('return_process')  

@user_passes_test(is_admin)
def shop_rejection(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    try:
        if request.method == "POST":
            if refund.return_status == 'Reject Evidence Submitted':
                    refund.return_status ='Return Approved'
                    refund.refund_title = 'Seller can offer partial refund or full refund or seller can ask customer to return product and provide full refund'
                    refund.buyer_return_status ='Return In Progress'
            elif refund.return_status == 'Evidence Submitted':
                    refund.return_status='Dispute Rejected'
                    refund.completed_date = Now()
                    refund.refund_title = 'Seller received item back, Buyer will be refunded with item amount'
                    refund.buyer_return_status='Return In Progress'
                    refund.seller_payment=0
                    refund.buyer_payment = refund.total_product_amount


            refund.updated_at = Now()
            refund.save()
            messages.success(request, "Seller dispute is rejected")
    except Exception as e:
         print(f'exception occured,{e}')
         messages.error(request, "exception raised")
    return redirect('return_process')  


def close_window_admin(request):
     return redirect('return_process')

@user_passes_test(is_admin)
def generateReturnShipping(request):
       
        today = date.today()

        vendors_ids = []
        order_ids = []
        refund = Refund.objects.filter(return_status__in=["Return ReadyToShip","Return Back ReadyToShip"],updated_at__gte=today)
        print("refund details are :",refund)
        for i in refund:
            if i.vendor.id not in vendors_ids:
                vendors_ids.append(i.vendor.id)
        for i in refund:
            if i.order.id not in order_ids:
                order_ids.append(i.order.id)
        #get parcel items for shipping
        parcel_data={}
        parcel_str = ''
        for i in refund:
            product = Product.objects.get(pk=i.orderproduct.product.id,vendor_id__in=vendors_ids)
            v_id = product.vendor.id
            if v_id in parcel_data:
                parcel_str = parcel_data[v_id]
                parcel_str = product.product_name[:30] + ','+ parcel_str
                parcel_data[v_id] = parcel_str
            else:
                parcel_str=''
                parcel_str = product.product_name[:30] + ','+ parcel_str 
                parcel_data[v_id] = parcel_str

        
        
        subweight=0
        total_weight={}
        for i in refund:
            product = Product.objects.get(pk=i.orderproduct.product.id,vendor_id__in=vendors_ids)
            v_id = product.vendor.id
            if v_id in total_weight:
                    subweight = total_weight[v_id]
                    subweight += (product.weight * i.quantity)
                    total_weight[v_id] = subweight
            else:
                subweight=0
                subweight += (product.weight * i.quantity)
                total_weight[v_id] = subweight
        
        

        subtotal=0
        total_data={}
        
        for i in refund:
            product = Product.objects.get(pk=i.orderproduct.product.id,vendor_id__in=vendors_ids)
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

        for v_id in vendors_ids:
            returnshipping =  Return_Shipping.objects.get(order_id__in=order_ids,vendor_id=v_id)
            returnshipping.parcel_content = parcel_data[v_id]
            returnshipping.weight_kg =  (total_weight[v_id]/1000)
            returnshipping.parcel_value =  total_data[v_id]  
            returnshipping.save()
               
    
        returnship_details = Return_Shipping.objects.filter(updated_at__gte=today)   
        print('returnship_details is :',returnship_details)
        context={
            'returnship_details' : returnship_details
        }
                
        return render(request,'admin/reurn_generate.html',context)

@user_passes_test(is_admin)
def vendor_payout(request):

    # date = datetime.datetime.today()
    # week = date.strftime("%V")

    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=7)

    some_day_last_week = date.today() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    stripe_const_charge = Mappings.objects.get(name='stripe_const_charge')
    stripe_fees_above_100 = Mappings.objects.get(name='stripe_fees_above_100')
    stripe_fees_below_100 = Mappings.objects.get(name='stripe_fees_below_100')
    platform_charge = Mappings.objects.get(name='general_platform_charge')

    orders = OrderProduct.objects.filter(completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['Completed','Cancelled Item','Cancelled Order']).values('order_id').distinct()

   
  
    for data in orders:  
        order_id = data.get('order_id') 
        vpout = VendorPayout.objects.filter(order_id = order_id ,is_ordered=True)
        for item in vpout:
            
                #calculate total amount of completed and cancelled items
                completed_query = OrderProduct.objects.filter(completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['Completed'],order = item.order, vendor = item.vendor)
                cancelled_query = OrderProduct.objects.filter(completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['Cancelled Item','Cancelled Order'],order = item.order, vendor = item.vendor)
                cancelled_sum = 0
                completed_sum = 0
                
                if  completed_query.exists():
                    completed_sum = completed_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total=Sum('total_product_amt')).first()
                if cancelled_query.exists():
                    cancelled_sum = cancelled_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total=Sum('total_product_amt')).first()

                if completed_sum: 
                    item.completed_item_amt =  completed_sum.get('total')
                else : 
                    item.completed_item_amt = 0

                if cancelled_sum :
                    item.cancelled_item_amt =  cancelled_sum.get('total')
                else : 
                    item.cancelled_item_amt = 0


                #calculate shipping fees
                total_weight=0
                for i in completed_query:
                    product = Product.objects.get(pk=i.product.id,vendor_id=i.vendor_id)
                    total_weight +=  (product.weight * i.quantity)
                item.parcel_weight = total_weight

                ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=total_weight,max_weight_limit__gte=total_weight)
                item.calc_shipcharge_cust = ship_cost.buyer_shipping_fees
                item.calc_shipcharge_seller = ship_cost.seller_shipping_fees

                if item.items_amount >= item.vendor.free_del_amount_limit:
                                        item.calc_shipcharge_seller = round((ship_cost.seller_shipping_fees + ship_cost.buyer_shipping_fees),2)
                                        item.calc_shipcharge_cust = 0
                
                return_fees = 0
                if cancelled_query.exists():
                    orderproduct = cancelled_query.first()
                    if orderproduct.status == 'Cancelled Order':
                        return_fees = item.shipchargepaid_by_cust
                        item.calc_shipcharge_seller = 0
                        item.calc_shipcharge_cust = 0

                #calculate platform fees
                print(item.completed_item_amt)
                print(platform_charge.value)
                item.platform_fees = round((item.completed_item_amt * platform_charge.value/100),2)

                #transaction_fees
                v_count = VendorPayout.objects.filter(order=item.order,is_ordered=True).count()
                if v_count > 2 :
                    stripe_const_charge = 0.10
                elif v_count >1 :
                    stripe_const_charge = 0.15
                else :
                    stripe_const_charge = 0.30 
            
                    
                trans_amt = item.completed_item_amt + item.cancelled_item_amt + item.shipchargepaid_by_cust
                if trans_amt < 100 :
                    item.stripe_transaction_fees = round((trans_amt * stripe_fees_below_100.value/100) ,2)
                else:
                    item.stripe_transaction_fees = round((trans_amt * stripe_fees_above_100.value/100) + stripe_const_charge,2)

                #calculate customer & vendor payout
                item.total_vendor_payout =  round(( item.completed_item_amt - item.stripe_transaction_fees - item.platform_fees - item.calc_shipcharge_seller),2)
                item.total_customer_payout = item.cancelled_item_amt + return_fees
                        
                #calculate shipping payout        
                item.total_shipping_payout = round((item.calc_shipcharge_seller + item.calc_shipcharge_cust),2)
                #calc shipping fees adjustment
                item.shipping_adjustment =  round((item.calc_shipcharge_seller + item.calc_shipcharge_cust - item.actual_shipping_cost),2) 
           
                item.Week_duration = monday_of_last_week
                   
                item.processed_flag = True

                item.save()
    
    vendorpout = VendorPayout.objects.filter(is_ordered=True)   
    vendor_name = request.GET.get('vendor_name', "")
    if vendor_name:
            vendorpout = vendorpout.filter(vendor__name = vendor_name)

    vendor = Vendor.objects.all()     
    context = {
            'vendorpayout' : vendorpout,
            'vendor' : vendor
        }
        
    return render(request, 'admin/vendor_payout.html',context)



@user_passes_test(is_admin)
def return_vendor_payout(request):

    
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=7)

    some_day_last_week = date.today() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    

    stripe_const_charge = Mappings.objects.get(name='stripe_const_charge')
    stripe_fees_above_100 = Mappings.objects.get(name='stripe_fees_above_100')
    stripe_fees_below_100 = Mappings.objects.get(name='stripe_fees_below_100')
    platform_charge = Mappings.objects.get(name='general_platform_charge')

    orders = Refund.objects.filter(completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,return_status__in=['ReadyToProcess','Dispute Approved','Return Request Cancelled','Return Back ReadyToShip','Dispute Rejected']).values('order_id').distinct()

    if orders :
        for data in orders:
            order_id = data.get('order_id') 
            vpout = Return_VendorPayout.objects.filter(order = order_id,is_ordered=True)
            for item in vpout:
                if item.process_flag == False :
                        #calculate total amount of completed and cancelled items
                        query = Refund.objects.filter(completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['ReadyToProcess','Dispute Approved','Return Request Cancelled','Return Back ReadyToShip','Dispute Rejected'],order = item.order, vendor = item.vendor)
                        if  query.exists():
                            seller_sum = query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total=Sum('seller_payment'))
                
                        if  query.exists():
                            buyer_sum = query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total=Sum('buyer_payment'))

                        if seller_sum: 
                            item.seller_payment_amt = seller_sum
                        else :
                            item.seller_payment_amt = 0

                        if buyer_sum: 
                            item.buyer_payment_amt = buyer_sum
                        else :
                            item.buyer_payment_amt = 0

                        #calculate platform fees
                        if item.seller_payment_amt :
                                item.platform_fees = round( (item.seller_payment_amt * platform_charge.value/100),2)

                        #calculate transaction fees
                        v_count = Return_VendorPayout.objects.filter(order=item.order,is_ordered=True).count()
                        if v_count > 2 :
                            stripe_const_charge = 0.10
                        elif v_count >1 :
                            stripe_const_charge = 0.15
                        else :
                            stripe_const_charge = 0.30 
                        #full order return
                        if item.order_status == "Return Requested":
                            if item.amt_paid_by_customer < 100 :
                                item.stripe_transaction_fees =  round((item.amt_paid_by_customer * stripe_fees_below_100.value/100) ,2)
                            else :
                                item.stripe_transaction_fees = round((item.amt_paid_by_customer * stripe_fees_above_100.value/100) + stripe_const_charge,2)

                        #partial order return
                        else:
                            trans_amount = item.buyer_payment_amt +item.seller_payment_amt
                            if trans_amount < 100 :
                                item.stripe_transaction_fees =  round((trans_amount * stripe_fees_below_100.value/100) ,2)
                            else :
                                item.stripe_transaction_fees = round((trans_amount * stripe_fees_above_100.value/100) + stripe_const_charge,2)

                        #calculate shipping charges
                    
                        buyer_parcel_weight = 0
                        seller_parcel_weight = 0
                        toseller_pickupdate_cnt = 0
                        tobuyer_pickupdate_cnt = 0
                        return_item_tobuyer_flag = False
                        return_item_toseller_flag = False

                        seller_query = Refund.objects.filter(order = item.order,vendor=item.vendor,returned_item_toseller = True,completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['ReadyToProcess','Dispute Approved','Return Request Cancelled','Return Back ReadyToShip','Dispute Rejected'])
                        buyer_query = Refund.objects.filter(order = item.order,vendor=item.vendor,returned_item_tobuyer = True,completed_date__gte=monday_of_last_week, completed_date__lt=monday_of_this_week,status__in=['ReadyToProcess','Dispute Approved','Return Request Cancelled','Return Back ReadyToShip','Dispute Rejected'])
                        
                        if seller_query.count() > 0 :
                            return_item_toseller_flag = True
                        if buyer_query.count() > 0 :
                            return_item_tobuyer_flag = True
                            
                        
                        if seller_query.exists():
                            seller_parcel = seller_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total_weight=Sum('product_total_weight')).first()
                            seller_parcel_weight = seller_parcel.get('total_weight')
                        
                        if buyer_query.exists():
                            buyer_parcel = buyer_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(total_weight=Sum('product_total_weight')).first()
                            buyer_parcel_weight = buyer_parcel.get('total_weight')

                    
                    
                        if seller_query.exists():
                            toseller_date = seller_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(date_count=Count('return_pickup_date',distinct=True)).first()
                            toseller_pickupdate_cnt = toseller_date.get('date_count')
                            
                                
                        if buyer_query.exists():
                                tobuyer_date = buyer_query.values('order_id','vendor_id').order_by('order_id','vendor_id').annotate(date_count=Count('returnback_pickup_date',distinct=True)).first()
                                tobuyer_pickupdate_cnt = tobuyer_date.get('date_count')

                        if item.order_status == "Return Requested":
                            first_time_cust_ship_fees = item.shipchargepaid_by_cust
                            first_time_seller_ship_fees = item.shipcharge_to_seller
                        else:
                            first_time_cust_ship_fees = 0
                            first_time_seller_ship_fees = 0

                        toseller_shipcharge_custmer = 0
                        toseller_shipcharge_seller = 0 
                        tobuyer_shipcharge_custmer = 0
                        tobuyer_shipcharge_seller = 0 
                        
                        if return_item_tobuyer_flag == True :
                            if toseller_pickupdate_cnt == 1 :
                                    if buyer_parcel_weight == seller_parcel_weight:
                                        ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=buyer_parcel_weight,max_weight_limit__gte=buyer_parcel_weight)
                                        shipcharge_custmer = ship_cost.buyer_shipping_fees
                                        shipcharge_seller = ship_cost.seller_shipping_fees
                                                                
                                        item.calc_shipcharge_seller = round(2 * (shipcharge_custmer + shipcharge_seller) + first_time_seller_ship_fees,2)
                                        item.calc_shipcharge_cust = first_time_cust_ship_fees
                                    
                                    else:
                                        ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=seller_parcel_weight,max_weight_limit__gte=seller_parcel_weight)
                                        toseller_shipcharge_custmer = ship_cost.buyer_shipping_fees
                                        toseller_shipcharge_seller = ship_cost.seller_shipping_fees  

                                        ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=buyer_parcel_weight,max_weight_limit__gte=buyer_parcel_weight)
                                        tobuyer_shipcharge_custmer = ship_cost.buyer_shipping_fees
                                        tobuyer_shipcharge_seller = ship_cost.seller_shipping_fees 

                                        item.calc_shipcharge_seller = round((tobuyer_shipcharge_custmer + tobuyer_shipcharge_seller) + toseller_shipcharge_seller + first_time_seller_ship_fees,2)
                                        item.calc_shipcharge_cust = round(toseller_shipcharge_custmer + first_time_cust_ship_fees,2)
                                        

                            else:
                                    refunds = seller_query.values('order_id','vendor_id','return_pickup_date').order_by('order_id','vendor_id','return_pickup_date').annotate(total_weight=Sum('product_total_weight'))
                                    for refund in refunds:
                                            pickdate = refund.get('return_pickup_date')
                                            weight = refund.get('total_weight')

                                            ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=weight,max_weight_limit__gte=weight)
                                            shipcharge_custmer = ship_cost.buyer_shipping_fees
                                            shipcharge_seller = ship_cost.seller_shipping_fees

                                            toseller_shipcharge_seller += shipcharge_seller
                                            toseller_shipcharge_custmer += shipcharge_custmer

                                    ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=buyer_parcel_weight,max_weight_limit__gte=buyer_parcel_weight)
                                    tobuyer_shipcharge_custmer = ship_cost.buyer_shipping_fees
                                    tobuyer_shipcharge_seller = ship_cost.seller_shipping_fees 
                                    
                                    if buyer_parcel_weight == seller_parcel_weight:
                                        item.calc_shipcharge_seller = round(toseller_shipcharge_seller + toseller_shipcharge_custmer + tobuyer_shipcharge_custmer + tobuyer_shipcharge_seller + first_time_seller_ship_fees,2)
                                        item.calc_shipcharge_cust = first_time_cust_ship_fees

                                    else:
                                        item.calc_shipcharge_seller = round(toseller_shipcharge_seller  + tobuyer_shipcharge_custmer + tobuyer_shipcharge_seller + first_time_seller_ship_fees,2)
                                        item.calc_shipcharge_cust = round(toseller_shipcharge_custmer + first_time_cust_ship_fees,2)
                        else:
                            if return_item_toseller_flag == True:
                                if toseller_pickupdate_cnt == 1 :
                                    ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=seller_parcel_weight,max_weight_limit__gte=seller_parcel_weight)
                                    shipcharge_custmer = ship_cost.buyer_shipping_fees
                                    shipcharge_seller = ship_cost.seller_shipping_fees
                                                                
                                    item.calc_shipcharge_seller = round( shipcharge_seller + first_time_seller_ship_fees,2)
                                    item.calc_shipcharge_cust = round(shipcharge_custmer + first_time_cust_ship_fees,2)
                            
                                else :
                                        refunds = seller_query.values('order_id','vendor_id','return_pickup_date').order_by('order_id','vendor_id','return_pickup_date').annotate(total_weight=Sum('product_total_weight'))
                                        for refund in refunds:
                                            pickdate = refund.get('return_pickup_date')
                                            weight = refund.get('total_weight')

                                            ship_cost = ShipCharge.objects.get(currier_type = 'Standard',min_weight_limit__lte=weight,max_weight_limit__gte=weight)
                                            shipcharge_custmer = ship_cost.buyer_shipping_fees
                                            shipcharge_seller = ship_cost.seller_shipping_fees

                                            toseller_shipcharge_seller += shipcharge_seller
                                            toseller_shipcharge_custmer += shipcharge_custmer    
                                        
                                        item.calc_shipcharge_seller = round(toseller_shipcharge_seller  + first_time_seller_ship_fees,2)
                                        item.calc_shipcharge_cust = round(toseller_shipcharge_custmer + first_time_cust_ship_fees,2)
                            else:
                                item.calc_shipcharge_seller =  first_time_seller_ship_fees
                                item.calc_shipcharge_cust = first_time_cust_ship_fees
                    
                        item.save()  

                        item.total_customer_payout = round(item.buyer_payment_amt - item.calc_shipcharge_cust,2)
                        item.total_vendor_payout = round(item.seller_payment_amt - item.calc_shipcharge_seller -item.stripe_transaction_fees - item.platform_fees,2)
                        item.total_shipping_payout = round(item.calc_shipcharge_cust + item.calc_shipcharge_seller,2)
                        item.save()

        
        context = {
                'vendorpayout' : vpout,
            }
        return render(request, 'admin/return_vendor_payout.html',context)
    else:
        return render(request, 'admin/return_vendor_payout.html')