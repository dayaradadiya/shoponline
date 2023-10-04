import datetime
import json
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Now
from  django.contrib.auth.decorators import login_required,user_passes_test
from django.views import View
from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_customer
from cart.views import sellprice
from customers.forms import ReturnForm
from customers.models import Address
from orders.models import Order, OrderProduct, Refund
from django.db.models import Count
from django.core.paginator import Page, EmptyPage,PageNotAnInteger,Paginator
from shipping.models import Return_Shipping, ShipCharge

from vendor.views import get_vendor_list, render_to_pdf

# Create your views here.
@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def cprofile(request):
    profile=get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid and user_form.is_valid():
            try:
                 profile_form.save()
            except:
                messages.error(request,'Input file type is not correct')
                return redirect('cprofile')
            user_form.save()
            messages.success(request,'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
            
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form' : profile_form,
        'user_form' : user_form,
        'profile' : profile,
    }
    return render(request,'customers/cprofile.html',context)

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')

    orderproducts = OrderProduct.objects.filter(user=request.user).order_by('-created_at')
    orderproducts_toship = OrderProduct.objects.filter(user=request.user,status__contains=("New")).order_by('-created_at')#to_ship
    orderproducts_shipped = OrderProduct.objects.filter(user=request.user,status__contains="PickedUpToDeliver").order_by('-created_at') #to_recieive
    orderproducts_delivered = OrderProduct.objects.filter(user=request.user,status__contains="Delivered").order_by('-created_at') #Delivered
    orderproducts_completed = OrderProduct.objects.filter(user=request.user,status__contains="Completed").order_by('-created_at') #Completed
    orderproducts_cancelled = OrderProduct.objects.filter(user=request.user,status__contains="Cancelled").order_by('-created_at') #Cancellation
    orderproducts_returned = OrderProduct.objects.filter(user=request.user,status__contains="Return").order_by('-created_at') #Return refund

    list_status = ["Return Approved","Return in Process","Return Request Cancelled","Return Requested"]
    paginator = Paginator(orderproducts,10)
    page = request.GET.get('page')
    paged_orderproducts = paginator.get_page(page)
    
    # tohsip
    paginator = Paginator(orderproducts_toship,10)
    page_toship = request.GET.get('page')
    paged_orders_toship = paginator.get_page(page_toship)

    # shipped
    paginator = Paginator(orderproducts_shipped,10)
    page_shipped = request.GET.get('page')
    paged_orders_shipped = paginator.get_page(page_shipped)

    # delivered
    paginator = Paginator(orderproducts_delivered,10)
    page_delivered = request.GET.get('page')
    paged_orders_delivered = paginator.get_page(page_delivered)

    # completed
    paginator = Paginator(orderproducts_completed,10)
    page_completed = request.GET.get('page')
    paged_orders_completed = paginator.get_page(page_completed)
    
    # cancelled
    paginator = Paginator(orderproducts_cancelled,10)
    page_cancelled = request.GET.get('page')
    paged_orders_cancelled = paginator.get_page(page_cancelled)

    # returned
    paginator = Paginator(orderproducts_returned,10)
    page_returned = request.GET.get('page')
    paged_orders_returned = paginator.get_page(page_returned)
    
    context= {
        'orderproducts' : paged_orderproducts,
        'orderproducts_toship'	:	paged_orders_toship,
        'orderproducts_shipped'	:	paged_orders_shipped,
        'orderproducts_delivered'	:	paged_orders_delivered,
        'orderproducts_completed'	:	paged_orders_completed,
        'orderproducts_cancelled'	:	paged_orders_cancelled,
        'orderproducts_returned'	:	paged_orders_returned,
        'list_status' : list_status,

    }

    return render(request, 'customers/my_orders.html',context)

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def order_details(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_product = OrderProduct.objects.filter(order=order)

        context = {
            'order' : order,
            'ordered_product' : ordered_product,
        }
        return render(request, 'customers/order_details.html',context)
    except:
        return redirect('customer')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')   
def address(request):

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
        return redirect("customer_address")
    context = {
        'address' : address
    }
    return render(request,'customers/address.html',context)


def make_address_default(request):
    id = str(request.GET['id'])
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean':True})


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def delete_customer_address(request,pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    messages.success(request,'Address has been deleted successfully!')
    return redirect('customer_address')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def edit_customer_address(request,pk):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    address_line_1 = request.POST.get("address_line_1")
    unit_no = request.POST.get("unit_no")
    postal_code = request.POST.get("postal_code")
    mobile = request.POST.get("mobile")
    country = request.POST.get("country")

    if len(mobile) > 8  :
        messages.error(request, 'Mobile no should be 8 digit long')
        return redirect('request_refund',pk)
    elif  first_name == '' or last_name == '' or address_line_1 == '' or unit_no == '' or  postal_code == '' or country == '' :
       messages.error(request, 'Please fill all address details')
       return redirect('request_refund',pk)
    
    Address.objects.filter(user=request.user,pk=pk).update(user=request.user,
        first_name=first_name,
        last_name=last_name,
        address_line_1=address_line_1,
        unit_no=unit_no,
        postal_code=postal_code,
        mobile=mobile,
        country=country)
    return redirect('customer_address')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def cancel_item_customer(request,order_number,id):
    cancel_reason = request.POST.get('cancel_reason')
    order = Order.objects.get(order_number=order_number,is_ordered=True)
    OrderProduct.objects.filter(pk=id,order_id=order.id).update(status="Cancelled Item",is_cancelled=True,completed_date=Now(),cancellation_reason=cancel_reason,updated_at=Now())

    v_id = []
    data = json.loads(order.total_data)
    for vendor_id in data :
        v_id.append(vendor_id)
    if len(v_id)<2 :
        product_count = OrderProduct.objects.filter(order_id=order.id).count()
        cancelled_count = OrderProduct.objects.filter(order_id=order.id,status__contains="Cancelled").count()
        if cancelled_count == product_count :
             order = Order.objects.get(order_number=order_number,is_ordered=True).update(status="Cancelled Order",is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
             OrderProduct.objects.filter(order_id=order.id).update(status="Cancelled Order",completed_date=Now(),is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
    
    return redirect('customer_my_orders')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def cancel_order_customer(request,order_number):
    cancel_reason = request.POST.get('cancel_reason')
    Order.objects.filter(order_number=order_number,is_ordered=True).update(status="Cancelled Order",is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
    OrderProduct.objects.filter(order__order_number = order_number).update(status="Cancelled Order",is_cancelled=True,completed_date=Now(),cancellation_reason=cancel_reason,updated_at=Now())
    
    return redirect('custorder_cancellation')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def custorder_cancellation(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True,status__in=('New','Packed')).order_by('-created_at')
    orders_count = orders.count()
    orderproducts = OrderProduct.objects.filter(user=request.user,status__in=('New','Packed')).order_by('-created_at')
    
    context = {
        'orders' : orders,
        'orders_count' : orders_count,
        'orderproducts' : orderproducts,
    }
    return render(request,'customers/cancellation.html',context)


@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def customer_my_returns(request):
    return_all = Refund.objects.filter(user=request.user).order_by('-updated_at')
    return_approved = Refund.objects.filter(user=request.user,return_status='Continue Return').order_by('-updated_at')
    completedprocess = ['ReadyToProcess','Return Request Cancelled','Return ReadyToShip']
    returnform = ReturnForm()

    paginator = Paginator(return_all,10)
    page = request.GET.get('page')
    page_return_all = paginator.get_page(page)
    
    # tohsip
    paginator = Paginator(return_approved,10)
    page_approved= request.GET.get('page')
    page_return_approved = paginator.get_page(page_approved)

    context = {
        'return_approved' : page_return_approved,
        'return_all' : page_return_all,
        'returnform' : returnform,
        'completedprocess' : completedprocess,
    }
    return render(request, 'customers/returns/my_returns.html',context)

  


class return_check_mychecklist(View):
    def get(self,request,*args,**kwargs):
        #print all products with invoice
        id_list = request.GET.getlist('boxes')
        return_pickup_date = request.GET.get('return_pickup_date')

        order_cnt = Refund.objects.filter(pk__in=id_list).aggregate(order_cnt = Count('order_id', distinct=True))["order_cnt"]
        
        if order_cnt > 1:
            messages.error(request,'Please select items belogs to one order at a time to download print label')
            return redirect('customer_my_returns')
        refund_main = Refund.objects.filter(pk__in=id_list)
        refund_main_cnt = refund_main.count()
        first_product = Refund.objects.filter(pk__in=id_list).first()
        address = Address.objects.get(user=request.user,status=True)
        for x in id_list:
                if Refund.objects.filter(pk=int(x),return_status="Return ReadyToShip").exists():
                     pass
                else:
                    Refund.objects.filter(pk=int(x)).update(return_status="Return ReadyToShip",returned_item_toseller = True,buyer_return_status='Return in Process',return_pickup_date=return_pickup_date,updated_at=Now())
                    refund = Refund.objects.get(pk=int(x))
                    OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return in Process",updated_at=Now())
                    
                    if Return_Shipping.objects.filter(order=refund.order, vendor=refund.vendor).exists() :
                        return_shipping = Return_Shipping.objects.get(order=refund.order, vendor=refund.vendor)
                    else:
                        return_shipping = Return_Shipping()
                    
                    return_shipping.order_id = refund.order.id     
                    return_shipping.vendor_id = refund.vendor_id

                    return_shipping.receiver_name = refund.vendor.vendor_name					
                    return_shipping.receiver_contact =	refund.vendor.user.phone_number		
                    return_shipping.receiver_email	= refund.vendor.user.email		
                    return_shipping.receiver_unit = refund.vendor.user.userprofile.unit_no		
                    return_shipping.receiver_postcode = refund.vendor.user.userprofile.pin_code	
                    return_shipping.receiver_company = refund.vendor.user.businessprofile.company_name
                    return_shipping.receiver_alt_contact = refund.vendor.user.userprofile.alt_phone_number		

                    return_shipping.sender_name =	address.full_name			
                    return_shipping.sender_contact = address.mobile
                    return_shipping.sender_email =	request.user.email	
                    return_shipping.sender_unit = address.unit_no
                    return_shipping.sender_postcode =address.postal_code
                    return_shipping.return_pickup_date = refund.return_pickup_date
                    return_shipping.save()

                    
        total = 0
        tax = 0
        grand_total = 0
        temp_total = 0
        
        if refund_main_cnt > 1:
            for cart_item in refund_main:
                    price = 0
                    discount = 0
                    orderproduct = OrderProduct.objects.get(id=cart_item.orderproduct.id)
                    if cart_item.variant :
                        
                        variant_price = cart_item.variant.variant_price
                        variant_discount = cart_item.variant.variant_discount
                        temp_total += (sellprice(variant_price,variant_discount) * orderproduct.quantity)
                        
                    else:
                        price = cart_item.product.price
                        discount = cart_item.product.discount
                        temp_total += (sellprice(price,discount) * orderproduct.quantity)
                    total = round(temp_total,2)

                #generate pdf
            data = {
                    'refund_main': refund_main,
                    'first_product' : first_product,
                    'total' : total,
                    'refund_main_cnt':refund_main_cnt,
                        }
            pdf = render_to_pdf('customers/pdf_template.html', data)

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" + Now()
            content = "attachment; filename='%s'" %(filename)
            response['Content-Dispositio'] = content 
            
            return response
        else:
             refund_main = Refund.objects.get(pk__in=id_list)
             orderproduct = OrderProduct.objects.get(id=refund_main.orderproduct.id)
             if first_product.variant :
                    variant_price = first_product.variant.variant_price
                    variant_discount = first_product.variant.variant_discount
                    temp_total = (sellprice(variant_price,variant_discount) * orderproduct.quantity)
             else:
                    price = first_product.product.price
                    discount = first_product.product.discount
                    temp_total = (sellprice(price,discount) * orderproduct.quantity)
             total = round(temp_total,2)
            
             print('refund_main is 2 :',refund_main)
             data = {
                'item':refund_main,
                'first_product': first_product,
                'total' : total,
                'refund_main_cnt' : refund_main_cnt,
            }
             pdf = render_to_pdf('customers/pdf_template.html', data)
             response = HttpResponse(pdf, content_type='application/pdf')
             filename = "Invoice_%s.pdf" + Now()
             content = "attachment; filename='%s'" %(filename)
             response['Content-Dispositio'] = content 

             return response

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')   
def return_readytoship(request,id):
    pickdate = Now() + datetime.timedelta(days=2) 
    Refund.objects.filter(pk=int(id)).update(return_status="Return ReadyToShip",buyer_return_status='Return in Process',updated_at=Now())
    refund = Refund.objects.get(pk=int(id))
    OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return in Process",updated_at=Now())
    #Shipping.objects.filter(order_id=order.id,vendor=get_vendor_list(request)).update(return_pickup_date=pickdate,updated_at=Now(),is_ordered=True)
    return redirect('customer_my_returns')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def mass_return_readytoship(request):
    if request.method == 'POST':
        pickdate = Now() + datetime.timedelta(days=2) 
        id_list = request.POST.getlist('readyboxes')
        
        for x in id_list:
            Refund.objects.filter(pk=int(x)).update(status="Return ReadyToShip",buyer_return_status='Return in Process',updated_at=Now())
            refund = Refund.objects.get(pk=int(x))
            OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return in Process",updated_at=Now())
    
            #Shipping.objects.filter(order_id=orderproduct.order.id,vendor=get_vendor_list(request)).update(return_pickup_date=pickdate,updated_at=Now(),is_ordered=True)
    return redirect('customer_my_returns')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def return_counter_amount(request,id):
    if request.method == 'POST':
        refund = Refund.objects.get(pk=int(id))
        orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)

        counteramount = request.POST.get('counteramount')
        if counteramount == '':
            messages.error(request,'Counter amount field must not be empty, please add counter amount and confirm.')
            return redirect('customer_my_returns')
        print('counteramount is :',counteramount)
        counteramt = float(counteramount)
        if counteramt > refund.total_product_amount :
                messages.error(request,'Counter amount should be less then item price')
                return redirect('customer_my_returns')
        print('counteramt is :',counteramt)
        refund.return_status='Countered Offer'
        refund.buyer_return_status='Countered Offer'
        refund.counter_amount = counteramt
        refund.updated_at = Now()
        refund.save()
        messages.success(request, 'Your proposal is submitted successfully.')
        return redirect('customer_my_returns')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def return_cust_accept_proposal(request,id):
    if request.method == 'POST':
        refund = Refund.objects.get(pk=int(id))
        orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
        refund.return_status='Customer Accepted Seller Proposal'
        refund.buyer_return_status = 'Return In Process'
        refund.updated_at = Now()
        refund.save()
        messages.success(request, 'Refund amount will be transfered to your account within a week.')
        return redirect('customer_my_returns')


def close_window(request):
    return redirect('customer_my_returns')

@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def customer_return_continue(request,id):

    if request.method == 'POST':
        refund = Refund.objects.get(pk=int(id))
        orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
        refund.return_status='Continue Return'
        refund.buyer_return_status = 'Return In Process'
        refund.updated_at = Now()
        refund.save()
        messages.success(request, 'You need to Return item, Parcel will be collected from your address, please select pick up date from To Pickup tab')
        return redirect('customer_my_returns')


@user_passes_test(check_role_customer)
@login_required(login_url = 'login')
def cancel_request(request,id):
    if request.method == 'POST':
        refund = Refund.objects.get(pk=int(id))
        refund.return_status="Return Request Cancelled"
        refund.buyer_return_status="Return Request Cancelled"
        refund.completed_date = Now()
        refund.refund_title="Buyer cancelled return request, seller payout will be processed"
        refund.updated_at=Now()
        refund.seller_payment = refund.total_product_amount
        refund.buyer_payment = 0
        refund.save()

        orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
        
        OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return Request Cancelled",completed_date = Now(),updated_at=Now())
        messages.info(request, "This return request is cancelled.")
        return redirect('customer_my_returns')