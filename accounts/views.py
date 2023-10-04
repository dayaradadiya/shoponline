import datetime
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models.functions import Now
from accounts.utils import detectUser,send_verification_email
from cart.models import Cart, CartItem
from cart.views import _cart_id
from customers.forms import  RefundForm
from customers.models import Address
from orders.models import Order, OrderProduct, Refund,  RefundImages
from store.models import  Product,   WishlistModel
from .utils import send_otp
from datetime import datetime
from .models import Bank_Account_Info, BusinessProfile, ICProfile, User, UserProfile
from accounts.forms import UserForm
from vendor.forms import VendorForm
from django.contrib import messages,auth
from  django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
import requests
from  django.contrib.auth.decorators import login_required,user_passes_test
import pyotp
from vendor.forms import VendorForm
import re
from .forms import  UserForm
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

# Create your views here.

# Restrict the vendor page from accessing the customer page
def check_role_vendor(user):
    if user.role == 1 :
        return True
    else:
        raise PermissionDenied


# Restrict the customer page from accessing the vendor page
def check_role_customer(user):
    if user.role == 2 :
        return True
    else:
        raise PermissionDenied


def admin_check(user):
   return user.is_superuser


def is_admin(user):
    return user.is_staff

def validatePassword(password):
    if len(password) > 8  and  len(password) < 15 :
        lowercase = False
        uppercare = False
        num = False
        special = False
        for char in password:
            if (char.islower()):
                lowercase = True
            if (char.isupper()):
                uppercare = True
            if (char.isdigit()):
                num = True
            if (char.isalnum()):
                special = True
        return lowercase and uppercare and num and special
    else:
        return False

        


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # create user using create_user method
           
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if validatePassword(password):
                    confirm_password = request.POST['confirm_password'] 
                    email = email.lower()
                    if password == confirm_password :
                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                        user.role = User.CUSTOMER
                        user.save()

                        # user_group = Group.objects.get(name='customer')

                        # user.groups.add(user_group)


                        #send verification email
                        mail_subject = "Please activate your account"
                        email_template = 'accounts/emails/account_verification_email.html'
                        send_verification_email(request,user,mail_subject,email_template)

                        messages.info(request, 'Your account has been registered successfully, Please click on the activation link sent to your email address to acitivate the user!')
                        print('User is created')
                        return redirect('registerUser')
                    else:
                        messages.error(request,'Password does not match!')
                        return redirect('registerUser')
                else:
                    
                   messages.error(request,'Password must be 8 to 15 character long, one uppercase letter, one lowercase letter, one digit and a special character')
                   return redirect('registerUser')
            
        else:
            messages.error(request,'Email or username is already exists.') 
            return redirect('registerUser')
    else:
        form = UserForm()
       
    context = {
            "registerform" : form,
        }
    return render(request,'accounts/login.html',context)



def registerUser_backup(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # create user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            # user_group = Group.objects.get(name='customer')

            # user.groups.add(user_group)


            #send verification email
            mail_subject = "Please activate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.info(request, 'Your account has been registered successfully, Please click on the activation link sent to your email address to acitivate the user!')
            print('User is created')
            return redirect('registerUser')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()
       
    context = {
            "form" : form,
        }
    return render(request,'accounts/registerUser.html',context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        # b_form = BusinessProfileForm(request.POST)
            
        if form.is_valid() and v_form.is_valid :
         
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if validatePassword(password):
                    confirm_password = request.POST['confirm_password']
                    email = email.lower()
                    if password == confirm_password :
                        user = User.objects.create_user(
                            first_name = first_name,
                            last_name = last_name,
                            username = username,
                            email = email,
                            password = password,
                        )
                        user.role = User.VENDOR
                        
                        user.save()

                        # user_group = Group.objects.get(name='vendor')

                        # user.groups.add(user_group)

                        
                        vendor = v_form.save(commit=False)
                        
                        vendor.user = user
                        vendor_name = v_form.cleaned_data['vendor_name']
                        vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
                        user_profile = UserProfile.objects.get(user=user)
                        vendor.user_profile = user_profile

                        stype = v_form.cleaned_data['stype']
                        vendor.stype = stype
                        vendor.save()
                        print('stye is :',stype)

                        icprofile = ICProfile()
                        icprofile.user=user
                        icprofile.save()

                        
                        bprofile = BusinessProfile()
                        bprofile.user=user
                        bprofile.save()

                        bank_info = Bank_Account_Info()
                        bank_info.user = user
                        bank_info.save()

                        # bprofile = b_form.save(commit=False)
                        # stype = b_form.cleaned_data['stype']
                        # bprofile.user = user
                        # bprofile.stype = stype
                        # bprofile.save()
                        # send verification email
                        mail_subject = "Please activate your account"
                        email_template = 'accounts/emails/account_verification_email.html'
                        send_verification_email(request,user,mail_subject,email_template)

                        messages.success(request,'Your account has been registered successfully! Please wait for the approval.')
                        return redirect('registerVendor')
                    else:
                        messages.error(request,'Password does not match!')
                        return redirect('registerVendor')
                else:
                    
                    messages.error(request,'Password must be 8 to 15 character long, one uppercase letter, one lowercase letter, one digit and a special character')
                    return redirect('registerVendor')

        else:
            print('form is invalid')
            print(form.errors)
            print(v_form.errors)
            messages.error(request,'Email or username is already exists.') 
            return redirect('registerVendor')
    else:
        form = UserForm()
        v_form = VendorForm()
        # b_form = BusinessProfileForm()
    context = {
        'form' : form,
        'v_form' : v_form ,
        # 'b_form' : b_form,
    }
    return render(request,'accounts/registerVendor.html',context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email,password=password)
            email = email.lower()
            if user is not None:
                request.session['email'] = email
                send_otp(request)
                messages.info(request,"Otp has been sent to your login email id")
                return redirect('otp')

            else:
                messages.error(request,'Invalid login credentials')
                return redirect('login')
        else:
            registerform = UserForm()
       
            context = {
                    "registerform" : registerform,
                }
            return render(request,'accounts/login.html',context)

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.session['email']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_untill = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_untill is not None:
            valid_until = datetime.fromisoformat(otp_valid_untill)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User,email=email)
                    auth.login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                        is_cart_item_exists  = CartItem.objects.filter(cart=cart).exists()
                        
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart=cart)  

                            # getting product variations by cart id
                            product_variation = []
                            for item in cart_item:
                                variation = item.variations.all()
                                product_variation.append(list(variation))

                            # Get the cart items from the user to access his product variations
                            cart_item = CartItem.objects.filter(user=user)
                            ex_var_list = []
                            id = []
                            for item in cart_item:
                                existing_variation = item.variations.all()
                                ex_var_list.append(list(existing_variation))
                                id.append(item.id)
                        
                            # product_variations = [2,4,5,7,8]
                            # ex_var_list = [4,3,6,7]
                            #get the common product variations
                            for pr in product_variation:
                                if pr in ex_var_list:
                                    index = ex_var_list.index(pr)
                                    item_id = id[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity += 1
                                    item.user = user
                                    item.save()
                                else:
                                    cart_item = CartItem.objects.filter(cart=cart)
                                    for item in cart_item:
                                        item.user = user
                                        item.save()
                    except:
                        pass
                    
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query = requests.utils.urlparse(url).query
                        # next = /cart/checkout
                        params = dict(x.split('=') for x in query.split('&'))

                        if 'email' in request.session:
                            del request.session['email']

                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                        
                    except:
                        messages.success(request,'You are now logged in.')
                        return redirect('myAccount')
                            
                else:
                    error_message = "Invalid one time password"
            else:
                error_message = "One time password has expired"
        else:
            error_message = "Ops.. Something went wrong"



    return render(request,'accounts/otp.html',{'error_message' : error_message})




def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device





# def login(request):
#     if request.user.is_authenticated:
#         messages.warning(request, 'You are already logged in!')
#         return redirect('myAccount')
#     else:
#         if request.method == 'POST':
#             email = request.POST['email']
#             password = request.POST['password']
#             user = auth.authenticate(email=email,password=password)

#             if user is not None:
#                 user = request.user
#                 device = get_user_totp_device(user)
#                 if not device:
#                         device = user.totpdevice.create(confirmed=False)
#                 url = device.config_url
#                 print('url is :',url)
    
#                 messages.info(request,"Otp has been sent to your login email id")
#                 # return redirect('otp')

#             else:
#                 messages.error(request,'Invalid login credentials')
#                 return redirect('login')
#         else:
#             registerform = UserForm()
       
#             context = {
#                     "registerform" : registerform,
#                 }
#             return render(request,'accounts/login.html',context)

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out.")
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    if 'email' in request.session:
        del request.session['email']
    user=request.user
    rediectUrl = detectUser(user)
    return redirect(rediectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]
    orders_count = orders.count()
    context = {
        'orders' : orders,
        'orders_count' : orders_count,
        'recent_orders' : recent_orders
    }
    return render(request,'accounts/custDashboard.html',context)

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)

    
    orders = Order.objects.filter(~Q(status__contains="Return") & ~Q(status__contains="Cancelled"),vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
   
    recent_orders = orders[:5]

    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()

        total_revenue = round(total_revenue,2)
  
    # current month's revenue
    current_month = datetime.now().month
    current_month_orders = orders.filter(~Q(status__contains="Return") & ~Q(status__contains="Cancelled"),vendors__in=[vendor.id],created_at__month=current_month)
   
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()

    context={
        'orders' : orders,
        'orders_count' : orders.count(),
        'recent_orders' : recent_orders,
        'total_revenue' : total_revenue,
        'current_month_revenue' : current_month_revenue,

    }
    return render(request,'accounts/vendorDashboard.html',context)

def activate(request,uidb64,token):
    #activate user by seetting is active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')
    
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = "Reset Your Password"
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, "Account does not exists")
            return redirect('forgot_password')
            # send_password_reset 
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('myAccount')
        

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']   
        if validatePassword(password):
            confirm_password = request.POST['confirm_password'] 

            if password == confirm_password :
                pk = request.session.get('uid')
                user = User.objects.get(pk=pk)
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('myAccount')
            else:
                messages.error(request,'Password does not match!')
                return redirect('reset_password')
        else :
            messages.error(request,'Password must be 8 to 15 character long, one uppercase letter, one lowercase letter, one digit and a special character')
            return redirect('reset_password')        

    return render(request, 'accounts/reset_password.html')

@login_required(login_url='login')
def request_refund(request,pk):
    order_product = OrderProduct.objects.get(pk=pk) #get product
    order = Order.objects.get(order_number=order_product.order.order_number)
    address = Address.objects.filter(user=request.user,status = True)
    if address.exists():
        active_address = Address.objects.get(user=request.user,status = True)
    else:
        active_address = Address.objects.filter(user=request.user).first()
        
    ref_code = order_product.ref_code
    if request.method == 'POST':
        term = request.POST.get("terms")
        if not term :
            messages.error(request, "Please check 'I have read and accepted the return policy to proceed further'")
            return redirect('request_refund',pk)
        else:
            form = RefundForm(request.POST,request.FILES)
            try:
                    if form.is_valid():
                        files = request.FILES.getlist("images")
                        
                        #edit the order
                    
                        order = Order.objects.get(order_number=order_product.order.order_number,is_ordered=True)
                        orderproduct = OrderProduct.objects.get(pk=pk)
                        
                        order.refund_requested = True
                        order.updated_at = Now()
                        order.save()
                        
                        orderproduct.refund_requested = True
                        orderproduct.status='Return Requested'
                        orderproduct.updated_at = Now()
                        orderproduct.save()

                        if Refund.objects.filter( order=order,orderproduct=orderproduct,user = request.user,vendor = orderproduct.vendor).exists():
                            messages.error(request,"Return request is already raised")
                            return redirect("customer_my_orders")
                        else:
                            refund = form.save(commit=False)

                        #store the refund
                        
                            refund.order = order
                            refund.user = request.user
                            refund.vendor = orderproduct.vendor
                            refund.product = orderproduct.product
                            refund.variant = orderproduct.variant
                            refund.orderproduct = orderproduct
                            refund.product_total_weight = orderproduct.product.weight * orderproduct.quantity
                            refund.quantity = orderproduct.quantity
                            refund.product_price =  orderproduct.product_price
                            refund.total_product_amount = round(orderproduct.quantity * orderproduct.product_price,2)
                            refund.ref_code = ref_code
                            refund.terms_accepted = True
                            
                            # if refund.main_reason_id == 4 :
                            #     refund.return_status = 'Validation In Process'
                            #     refund.buyer_return_status = 'Validation In Process'
                            # else :
                            refund.return_status = 'Return Requested'
                            refund.buyer_return_status = 'Return Requested'

                            refund.save()

                            # daya start

                            orderproduct = OrderProduct.objects.get(pk=pk,order_id=order.id)

                            
                           
                            vendor_ids = []
                            orderp = OrderProduct.objects.filter(order_id = orderproduct.order.id)
                            for op in orderp:
                                if op.vendor.id not in vendor_ids:
                                    vendor_ids.append(op.vendor_id)

                            if len(vendor_ids) < 2:
                                products_cnt = OrderProduct.objects.filter(order_id = orderproduct.order.id,vendor_id__in = vendor_ids).count()
                                products_returned_cnt = OrderProduct.objects.filter(order_id = orderproduct.order.id,vendor_id__in = vendor_ids,status="Return Requested").count()

                                if products_cnt == products_returned_cnt :
                                    Order.objects.filter(id=orderproduct.order.id,is_ordered=True).update(status="Return Requested",refund_requested=True,updated_at=Now())
                                   
                            
                            
                            for i in files:
                                    refundimages = RefundImages.objects.create(refund=refund, image=i)
                                    refundimages.save()
                        
                            messages.info(request,"Your request is received, Seller will evaluate the request and will update in 3 days, please check status in My Returns.")
                            return redirect("customer_my_orders")
                    
            except Exception as e:
                            print(f'exception {e}')
                            messages.error(request,"Wrong files uploaded")
                            return redirect("customer_my_orders")
    else:
          default_values = {
                        'ref_code' :ref_code ,

            }

          form=RefundForm(initial=default_values)

    context = {
              'form' : form,
              'item' : order_product,
              'order' : order,
              'active_address' :active_address,
          }
    return render(request, "customers/request_refund.html",context)

def htmx_reason(request):
    form = RefundForm(request.GET)
    return HttpResponse(form["reason"])    


@login_required(login_url='login')
def wishlist_view(request):
    wishlist = WishlistModel.objects.filter(user=request.user)
    context = {
        'wishlist' : wishlist,
    }
    return render(request,'accounts/wishlist.html',context)
                  

def remove_wishlist_item(request,product_id,item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        item = WishlistModel.objects.get(user=request.user,id=item_id)
    
        item.delete()
    return redirect('wishlist_view')


def change_refund_address(request,itemid,id):

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    address_line_1 = request.POST.get("address_line_1")
    unit_no = request.POST.get("unit_no")
    postal_code = request.POST.get("postal_code")
    mobile = request.POST.get("mobile")
    country = request.POST.get("country")

    if len(mobile) > 8  :
        messages.error(request, 'Mobile no should be 8 digit long')
        return redirect('request_refund',itemid)
    elif  first_name == '' or last_name == '' or address_line_1 == '' or unit_no == '' or  postal_code == '' or country == '' :
       messages.error(request, 'Please fill all address details')
       return redirect('request_refund',itemid)
    
    orderoproduct = OrderProduct.objects.get(id=itemid)
    Address.objects.filter(user=request.user,pk=id).update(user=request.user,
        first_name=first_name,
        last_name=last_name,
        address_line_1=address_line_1,
        unit_no=unit_no,
        postal_code=postal_code,
        mobile=mobile,
        country=country)
    

    return redirect('request_refund',orderoproduct.id)  

