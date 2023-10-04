import json
from sre_constants import MAGIC
from urllib.parse import urlencode
import zipfile
from django.forms import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import Q
from django.db.models.functions import Now
from django.db.models import Count
from accounts.forms import BankAccForm, ICProfileForm, UserProfileForm
from accounts.models import Bank_Account_Info, BusinessProfile, ICProfile, UserProfile
from accounts.views import check_role_vendor
from cart.views import sellprice
from category.models import Category, Fourth_Level_Category, Main_Category,  Sub_Category, Vendor_Category, Vendor_Main_Category, Vendor_Sub_Category
from customers.forms import ReturnForm
from customers.models import Address
from mass_upload.models import Stock_keeping_unit
# from mass_upload.models import Stock_keeping_unit
from orders.models import DisputeImages, Order, OrderProduct, Refund, ReturnDispute
from shipping.models import Return_Shipping, ShipCharge, Shipping
from store.models import Images, Product, Specification, Variants
from vendor.forms import BPForm, CategoryForm,  DisputeImage_Form,  ImageForm, MainCategoryForm, ProductForm,   SpecificationForm, SubCategoryForm, VariantsForm, VendForm, VendorForm
from vendor.models import Vendor
from django.contrib import messages
from  django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator
import datetime
import magic
from django.db.models.functions import Lower
from django.http import HttpResponse
import io
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor
# Create your views here.


def get_vendor_list(request):
    try:
     vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile_backup(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form' : vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)
    if vendor.stype == 2 :
         businessprofile = get_object_or_404(BusinessProfile,user=request.user)
    if vendor.stype == 1 :
        ic_profile = get_object_or_404(ICProfile,user=request.user)
 
    
    if vendor.stype == 1 : 
        try:
            if request.method == 'POST':   
                profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
                vendor_form = VendForm(request.POST,request.FILES,instance=vendor)
                ic_form = ICProfileForm(request.POST,request.FILES,instance=ic_profile)
                # bp_form = BPForm(instance=businessprofile)
                if profile_form.is_valid() and vendor_form.is_valid() and ic_form.is_valid() :
                    profile_form.save()
                    vendor_form.save()

                    ic_form.save()

                    messages.success(request,'Settings updated.')
                    return redirect('vprofile')
                else:
                    print(profile_form.errors)
                    print(vendor_form.errors)
                    print(ic_form.errors)
            else:
                profile_form = UserProfileForm(instance=profile)
                vendor_form = VendForm(instance=vendor)
                ic_form = ICProfileForm(instance=ic_profile)

            context = {
            'profile_form': profile_form,
            'vendor_form' : vendor_form,
            'profile':profile,
            'vendor':vendor,
            'ic_form': ic_form,
            'ic_profile' : ic_profile,
            }
        except Exception as e:
            print(f'exception {e}')
            messages.error(request,"Issue in updating ICprofile")
             

    if vendor.stype == 2:
        if request.method == 'POST':
            profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
            vendor_form = VendForm(request.POST,request.FILES,instance=vendor)
            bp_form = BPForm(request.POST,request.FILES,instance=businessprofile)
            # ic_form = ICProfileForm()
            if profile_form.is_valid() and vendor_form.is_valid() and bp_form.is_valid() :
                profile_form.save()
                vendor_form.save()
                bp_form.save()
                messages.success(request,'Settings updated.')
                return redirect('vprofile')
            else:
                print(profile_form.errors)
                print(vendor_form.errors)
                print(bp_form.errors)
        else:
            profile_form = UserProfileForm(instance=profile)
            vendor_form = VendForm(instance=vendor)
            bp_form = BPForm(instance=businessprofile)

        context = {
        'profile_form': profile_form,
        'vendor_form' : vendor_form,
        'bp_form' : bp_form,
        'profile':profile,
        'vendor':vendor,
        'businessprofile' : businessprofile,
        }

    return render(request,'vendor/vprofile.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vaccount(request):
    bank_info = get_object_or_404(Bank_Account_Info,user=request.user)
    if request.method == 'POST':
            bank_acc_form = BankAccForm(request.POST,request.FILES,instance=bank_info)
            # ic_form = ICProfileForm()
            if  bank_acc_form.is_valid():
                bank_details = bank_acc_form.save(commit=False)
                bank_details.user = request.user
                bank_details.save()

                messages.success(request,'Account information is updated successfully')
                return redirect('vaccount')
            else:
                print(bank_acc_form.errors)
    else:
        
        bank_acc_form = BankAccForm(instance=bank_info)

    context = {
        'bank_acc_form' : bank_acc_form,
        'bank_info' : bank_info,
        }

    return render(request,'vendor/vaccount.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_builder(request):

    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "")

    vendor = Vendor.objects.get(user=request.user)
    products = Product.objects.filter(vendor=vendor,is_active=True).order_by('-id')
    product_count = products.count()

    if ordering:
            products = products.order_by(ordering) 

    if price:
            products = products.filter(price__lt = price)

    paginator = Paginator(products,10)
    page_products = request.GET.get('page')
    paged_products = paginator.get_page(page_products)

    

    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request,'vendor/product_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product_backup(request):

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        i_form = ImageForm(request.POST,request.FILES)
        files = request.FILES.getlist("images")
        if form.is_valid():
            vendor = Vendor.objects.get(user=request.user)
            if Product.objects.filter(product_name = product_name, vendor=vendor,is_active=True).exists():
                 messages.info(request,"Product with same name is already exists...")
                 return redirect('add_product')
            else:
                product_name = form.cleaned_data['product_name']
                product = form.save(commit=False)
                product.vendor = Vendor.objects.get(user=request.user)
                product.slug = slugify(product_name)
                product.save()

                for i in files:
                    productimages = Images.objects.create(product=product, image=i)
                    productimages.save()
            
                messages.success(request, 'Product added successfully!')
                return redirect('product_builder')
        else:
                print(form.errors)  
                print(i_form.errors)  
    else:
        form = ProductForm()
        i_form = ImageForm()

    context = {
        'form' : form,
        'i_form' : i_form,

    }
    return render(request,'vendor/add_product.html',context)


def activate_product(product):
    if product.variant == 'Color' :
        if Variants.objects.filter(Q(color_id__isnull=True),product=product).exists():
            product.is_active = False
        else :
            product.is_active = True
    elif product.variant == 'Size' :
        if Variants.objects.filter(Q(size_id__isnull=True) ,product=product).exists():
            product.is_active = False
        else :
            product.is_active = True
    elif product.variant == 'Size-Color' :
        if Variants.objects.filter(Q(size_id__isnull=True) & Q(color_id__isnull=True),product=product).exists():
            product.is_active = False
        else :
            product.is_active = True
   
    elif product.variant == 'None' :
        product.is_active = True
    else :
            product.is_active = True
    product.save()
    return

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        i_form = ImageForm(request.POST,request.FILES)
        variant_form = VariantsForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("images")

        #daya validation
        vartype = request.POST.get("variant")
        title = request.POST.get("title")
        color = request.POST.get("color")
        size = request.POST.get("size")
        
        if vartype == 'Color' :
            image_variant = request.POST.get("image_variant")
            price = request.POST.get("variantprice")
            if color == '' or title == '' or price == '' or image_variant == '':
                messages.error(request, "Variant color, title, price and image info is not filled")
                return redirect('add_product')
        elif vartype == 'Size':
            price = request.POST.get("variantprice")
            if size == '' or title == '' or price == '' :
                messages.error(request, "Variant size, title, price and image info is not filled")
                return redirect('add_product')
        elif vartype == 'Size-Color' :
            price = request.POST.get("variantprice")
            image_variant = request.POST.get("image_variant")
            if color == '' or size == '' or title == '' or price == '' or image_variant == '':
                messages.error(request, "Variant color, size, title, price and image info is not filled")
                return redirect('add_product')

        if form.is_valid() and variant_form.is_valid():
            product_name = form.cleaned_data['product_name']
            vendor = Vendor.objects.get(user=request.user)
            if Product.objects.filter(product_name = product_name, vendor=vendor,is_active=True).exists():
                 messages.info(request,"Product with same name is already exists...")
                 return redirect('add_product')
            else:
                product = form.save(commit=False)
                product.vendor = Vendor.objects.get(user=request.user)
                product.slug = slugify(product_name)
                if not product.fourth_level_category :
                     product.fourth_level_category = Fourth_Level_Category.objects.get(id=1660)
                product.save()
                
                Stock_keeping_unit.objects.create(product =  product,
                                                                  vendor = vendor)
                if product.variant != 'None' :
                    variant = variant_form.save(commit=False)
                    variant.product = product
                    variant.save()
                    
                    sku = Stock_keeping_unit.objects.get(product=product,vendor=vendor)
                    sku.variant = Variants.objects.get(product=product)
                    sku.save()
                activate_product(product)            
                
                
                for i in files:
                        Images.objects.create(product=product, image=i)

                try:
                     obj = Vendor_Main_Category.objects.get(vendor=product.vendor,name= product.main_category.name)
                except Vendor_Main_Category.DoesNotExist:
                     Vendor_Main_Category.objects.create(name=product.main_category.name,
                                             vendor=product.vendor,
                                             slug = slugify(product.main_category.name))
                vend_maincat = Vendor_Main_Category.objects.get(vendor=product.vendor,name= product.main_category.name)
                try:
                     obj_cat = Vendor_Category.objects.get(vendor=product.vendor,name=product.category.name,main_category_id=vend_maincat.id)
                except Vendor_Category.DoesNotExist:
                     Vendor_Category.objects.create(name=product.category.name,
                                                   main_category_id = vend_maincat.id,
                                             vendor=product.vendor,
                                             slug = slugify(product.category.name))
                cat = Vendor_Category.objects.get(vendor=product.vendor,name=product.category.name,main_category_id=vend_maincat.id)
                try:
                     obj_subcat = Vendor_Sub_Category.objects.get(vendor=product.vendor,name=product.sub_category.name,category_id=product.category.id,main_category_id=vend_maincat.id)
                except Vendor_Sub_Category.DoesNotExist:
                     Vendor_Sub_Category.objects.create(name=product.sub_category.name,
                                             vendor=product.vendor,
                                             main_category_id = vend_maincat.id,
                                             category_id = cat.id,
                                             slug = slugify(product.sub_category.name))

             
                     
            
                messages.success(request, 'Product added successfully!')
                return redirect('product_builder')
                
        else:
                print(form.errors)  
                print(i_form.errors)  
                print(variant_form.errors)
                
    else:
        form = ProductForm()
        i_form = ImageForm()
        variant_form = VariantsForm()

    context = {
        'form' : form,
        'i_form' : i_form,
        'variant_form' : variant_form,

    }
    return render(request,'vendor/add_product.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product_main(request,pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        
        form = ProductForm(request.POST or None,request.FILES or None,instance = product)
        if form.is_valid():
                product_name = form.cleaned_data['product_name']
                product = form.save(commit=False)
                product.vendor = Vendor.objects.get(user=request.user)
                product.slug = slugify(product_name)
                if not product.fourth_level_category :
                     product.fourth_level_category = Fourth_Level_Category.objects.get(id=1660)
                product.save()
                
                messages.success(request, 'Product updated successfully!')
                return redirect('edit_product',product.id)
        else:
            print(form.errors)  
    else: 
        form = ProductForm(instance=product)
    context = {
            'form' : form, 
            'product': product,
            
        }
    return render(request,'vendor/edit_product_main.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request,'Product has been deleted successfully!')
    return redirect('product_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request,pk):
     product = get_object_or_404(Product,pk=pk)
    #  images= Images.objects.filter(product=product)
     variants = Variants.objects.filter(product=product)
     form = VariantsForm(request.POST or None, request.FILES or None)
     form.fields['image_id'].queryset = Images.objects.raw('select id from store_images WHERE product_id=%s' ,[product.id])
     
     if request.method == 'POST':
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product
            variant.save()
            return redirect('detail_variant',pk=variant.id)

        else:
            print(form.errors)
            return render(request,'vendor/partials/variant_form.html',{ "form":form })
        
     context = {
         'form' : form,
         'product' : product,
         'variants':variants,
     } 

     return render(request,'vendor/edit_product.html',context)     


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_variant(request,pk):
    variant = Variants.objects.get(pk=pk)
    form = VariantsForm(request.POST or None, request.FILES or None, instance=variant)
    if request.method == 'POST':
        if form.is_valid():
            variant = form.save()
                    # if 'img' in request.FILES:
                    #     variant.image_variant = request.FILES['img']
                        # variant.save()
            return redirect('detail_variant',pk=variant.id)
    
    context = {
        "form" : form,
        "variant" : variant,
    }
    return render(request,"vendor/partials/variant_form.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def create_variant_form(request):
    context = {
        "form" : VariantsForm()
    }
    return render(request,"vendor/partials/variant_form.html",context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def detail_variant(request,pk):
    variant = Variants.objects.get(pk=pk)
    context = {
        'variant' : variant
    }
    return render(request,"vendor/partials/detail_variant.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_variant(request,pk):
    variant = Variants.objects.get(pk=pk)
    variant_cnt = Variants.objects.filter(product=variant.product).count()
    if variant_cnt < 2 :
        HttpResponse('One variant should be available with product')
    else:     
        variant.delete()
    return HttpResponse('')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_image(request,pk):
     
     product = get_object_or_404(Product,pk=pk)
     images = Images.objects.filter(product=product)
     imageform = ImageForm(request.POST or None,request.FILES or None)
     
     if request.method == 'POST':

        imageform = ImageForm(request.POST,request.FILES)
        if imageform.is_valid():
            # image = Images.objects.create(product=product, image=file)
            image = imageform.save(commit=False)
            image.product = product
            image.save()
            return redirect('detail_image',pk=image.id)
        else:
            print(imageform.errors)
            return render(request,'vendor/partials/image_form.html',{ "imageform":imageform })
        
     context = {
         'imageform' : imageform,
         'product' : product,
         'images':images,
     } 

     return render(request,'vendor/edit_image.html',context)     

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def create_image_form(request):
    context = {
        'imageform' : ImageForm(),
    }
    return render(request,"vendor/partials/image_form.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def detail_image(request,pk):
    image=Images.objects.get(pk=pk)
    context = {
        'image' : image,
    }
    return render(request,"vendor/partials/detail_image.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_image(request,pk):
    image = Images.objects.get(pk=pk)
    image_cnt = Images.objects.filter(product=image.product).count()
    if image_cnt < 2 :
        HttpResponse('One variant should be available with product')
    image.delete()
    return HttpResponse('')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_image(request,pk):
    image = Images.objects.get(pk=pk)
    imageform = ImageForm(request.POST or None, request.FILES or None, instance=image)
    if request.method == 'POST':
        if imageform.is_valid():
            image = imageform.save()
           
            return redirect('detail_image',pk=image.id)
        
        
    context = {
        "imageform" : imageform,
        "image" : image,
    }
    return render(request,"vendor/partials/image_form.html",context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def detail_picture(request,pk):
    image=Images.objects.get(pk=pk)
    context = {
        'image' : image,
    }
    return render(request,"vendor/partials/detail_picture.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def order_details(request,order_number):
    # try:
        order = Order.objects.get(order_number=order_number,is_ordered=True )
        ordered_product = OrderProduct.objects.filter(order=order,product__vendor=get_vendor_list(request))
        
        context = {
            'order' : order,
            'ordered_product' : ordered_product,
        }
    # except:
    #     return redirect('vendor')
        return render(request,'vendor/order_details.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    # order = Order.objects.filter(vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
 
    orderproducts_new = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="New").order_by('-created_at')
    orderproducts_packed = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="Packed").order_by('-created_at')
    orderproducts_readytoship = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="ReadyToShip").order_by('-created_at')
   
    paginator = Paginator(orderproducts_new,10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    order_count = orderproducts_new.count()

    paginator = Paginator(orderproducts_packed,10)
    page_packed = request.GET.get('page')
    paged_packed_orders = paginator.get_page(page_packed)


    paginator = Paginator(orderproducts_readytoship,10)
    page_readytoship = request.GET.get('page')
    paged_orders_readytoship = paginator.get_page(page_readytoship)

    context= {
        'order_count' :order_count,
        'orderproducts_new' : paged_orders,
        'orderproducts_packed' : paged_packed_orders,
        'orderproducts_readytoship' : paged_orders_readytoship,
    }
    
    return render(request,'vendor/my_orders.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def address(request):

    address = Address.objects.filter(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address_line_1 = request.POST.get("address_line_1")
        unit_no = request.POST.get("unit_no")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")
        mobile = request.POST.get("mobile")

        Address.objects.create(user=request.user,
                                            first_name=first_name, 
                                            last_name=last_name,
                                            address_line_1=address_line_1,
                                            unit_no=unit_no,
                                            postal_code=postal_code,
                                            country=country,
                                            mobile=mobile)
        messages.success(request,'Address added successfully.')
        return redirect("vendor_address")
    context = {
        'address' : address
    }
    return render(request,'vendor/address.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_vendor_address(request,pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    messages.success(request,'Address has been deleted successfully!')
    return redirect('vendor_address')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_vendor_address(request,pk):
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
    return redirect('vendor_address')


     
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def category_module(request):
    form = ProductForm(request.GET)

    return HttpResponse(form['category'])




@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def sub_category_module(request):
    form = ProductForm(request.GET)

    return HttpResponse(form['sub_category'])

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fourth_level_category_module(request):
    form = ProductForm(request.GET)

    return HttpResponse(form['fourth_level_category'])


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fifth_level_category_module(request):
    form = ProductForm(request.GET)

    return HttpResponse(form['fifth_level_category'])

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_specn(request,pk):
    product = get_object_or_404(Product,pk=pk)
    specns = Specification.objects.filter(product=product)
    specnform = SpecificationForm(request.POST or None)

    category = Category.objects.get(id=product.category.id)
    if product.sub_category :
        sub_category = Sub_Category.objects.get(id = product.sub_category.id)
    else :
        sub_category= ''
    if product.fourth_level_category:
         fourth_level_category = Fourth_Level_Category.objects.get(id = product.fourth_level_category.id)
    else:
        fourth_level_category=''
    if request.method == 'POST':

        specnform = SpecificationForm(request.POST)
        if specnform.is_valid():
            # image = Images.objects.create(product=product, image=file)
            specn = specnform.save(commit=False)
            specn.product = product
            specn.category_id = product.category.id
            if product.sub_category:
                specn.sub_category_id = product.sub_category.id
            if product.fourth_level_category:
                specn.fourth_level_category_id = product.fourth_level_category.id
            specn.save()
            return redirect('detail_specn',pk=specn.id)
        else:
            print(specnform.errors)
            return render(request,'vendor/partials/specn_form.html',{ "specnform":specnform })
        
    context = {
         'specnform' : specnform,
         'product' : product,
         'specns' : specns,
         'category' : category,
         'sub_Category' : sub_category,
         'fourth_level_category' : fourth_level_category
     } 
    

    return render(request,'vendor/edit_specn.html',context)    


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def create_specn_form(request,pk):

    product = get_object_or_404(Product,pk=pk)
    category = Category.objects.get(id=product.category.id)
    if product.sub_category:
         sub_category = Sub_Category.objects.get(id = product.sub_category.id)
    else:
        sub_category=''
    if product.fourth_level_category:
         fourth_level_category = Fourth_Level_Category.objects.get(id = product.fourth_level_category.id)
    else:
        fourth_level_category=''
    

    context = {
        'specnform' : SpecificationForm(),
        'category' : category,
        'sub_category' : sub_category,
        'fourth_level_category' : fourth_level_category,
    }
    return render(request,"vendor/partials/specn_form.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def detail_specn(request,pk):
    specn=Specification.objects.get(pk=pk)
    context = {
        'specn' : specn,
    }
    return render(request,"vendor/partials/detail_specn.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_specn(request,pk):
    specn = Specification.objects.get(pk=pk)
    specn.delete()
    messages.info(request, 'Product specifications are deleted successfully')
    return HttpResponse('')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_specn(request,pk):
        
        specn = Specification.objects.get(pk=pk)
        specnform = SpecificationForm(request.POST or None,  instance=specn)
        category = Category.objects.get(id=specn.product.category.id)

        if specn.sub_category:
         sub_category = Sub_Category.objects.get(id = specn.product.sub_category.id)
        else:
            sub_category=''
        if specn.fourth_level_category:
            fourth_level_category = Fourth_Level_Category.objects.get(id = specn.product.fourth_level_category.id)
        else:
            fourth_level_category=''
        

        if request.method == 'POST':
                    if specnform.is_valid():
                        specn = specnform.save()
                        return redirect('detail_specn',pk=specn.id)
         
            
        context = {
            "specnform" : specnform,
            "specn" : specn,
            'category' : category,
            'sub_category' : sub_category,
            'fourth_level_category' :fourth_level_category
        }
        return render(request,"vendor/partials/specn_form.html",context)


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f[0], f[1])

    return mem_zip.getvalue()

data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

#Opens up page as PDF

class order_pdf(View):
        def get(self, request, *args, **kwargs):
            Order.objects.filter(order_number=self.kwargs['order_number'],is_ordered=True).update(status="Packed",updated_at=Now())
            ordered_products = OrderProduct.objects.filter(pk=self.kwargs['id'],product__vendor=get_vendor_list(request))
            OrderProduct.objects.filter(pk=self.kwargs['id']).update(status="Packed",updated_at=Now())

            first_product = OrderProduct.objects.get(pk=self.kwargs['id'],product__vendor=get_vendor_list(request))

            if first_product.variant :
                    price = first_product.variant.variant_price
                    discount = first_product.variant.variant_discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            else:
                    price = first_product.product.price
                    discount = first_product.product.discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            total = round(temp_total,2)
            
            data = {
                # 'order' : order,
                'ordered_products':ordered_products,
                'first_product' : first_product,
                'total' : total,
            }

            pdf = render_to_pdf('vendor/pdf_template.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
            

#Automaticly downloads to PDF file

class download_pdf(View):
	def get(self, request, *args, **kwargs):
            order = Order.objects.get(order_number=self.kwargs['order_number'],is_ordered=True )
            ordered_products = OrderProduct.objects.filter(pk=self.kwargs['id'],product__vendor=get_vendor_list(request))
            first_product = OrderProduct.objects.get(pk=self.kwargs['id'],product__vendor=get_vendor_list(request))

            if first_product.variant :
                    price = first_product.variant.variant_price
                    discount = first_product.variant.variant_discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            else:
                    price = first_product.product.price
                    discount = first_product.product.discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            total = round(temp_total,2)
            
            data = {
                'order' : order,
                'ordered_products':ordered_products,
                'first_product': first_product,
                'total' : total,
            }
            pdf = render_to_pdf('vendor/pdf_template.html', data)

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %self.kwargs['id']
            content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        
        
# def check_mychecklist(request):
#     if request.method == 'POST':
#         id_list = request.POST.getlist('boxes')
#         for x in id_list:
#             OrderProduct.objects.filter(pk=int(x)).update(status="Packed",updated_at=Now())
#         return redirect('vendor_my_orders')

      
class check_mychecklist_backup(View):
    def get(self,request,*args,**kwargs):
        #print all products with invoice
        id_list = request.GET.getlist('boxes')
        orderedproducts = OrderProduct.objects.filter(pk__in=id_list,product__vendor=get_vendor_list(request))


        for x in id_list:
                OrderProduct.objects.filter(pk=int(x)).update(status="Packed",updated_at=Now())
                orderproduct = OrderProduct.objects.get(pk=int(x))
                Order.objects.filter(order_number=orderproduct.order.order_number,is_ordered=True).update(status="Packed",updated_at=Now())
        
        o_num = []
        for i in orderedproducts:
            if i.order.order_number not in o_num:
                o_num.append(i.order.order_number)
            
       
        for i in o_num:
            ordered_products = orderedproducts.filter(order__order_number=i)
            #calculate total price
            tax = 0
            grand_total = 0
            temp_total = 0
            for cart_item in ordered_products:
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

            #generate pdf
            data = {
                        'ordered_products':ordered_products,
                        'total' : total,
                    }
            pdf = render_to_pdf('vendor/pdf_template.html', data)

            # response = HttpResponse(pdf, content_type='application/pdf')
            # filename = "Invoice_%s.pdfn" + i
            # content = "attachment; filename='%s'" %(filename)
            # response['Content-Dispositio'] = content 
            files.append((i + ".pdf", pdf))

        full_zip_in_memory = generate_zip(files)

        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('attendnace.zip')

        return response


class check_mychecklist(View):
    def get(self,request,*args,**kwargs):
        #print all products with invoice
        id_list = request.GET.getlist('boxes')
        orderedproducts = OrderProduct.objects.filter(pk__in=id_list,product__vendor=get_vendor_list(request))

        
        order_cnt = OrderProduct.objects.filter(pk__in=id_list).aggregate(order_cnt = Count('order_id', distinct=True))["order_cnt"]
        
        if order_cnt > 1:
            messages.error(request,'Please select items belogs to one order at a time to print label')
            return redirect('vendor_my_orders')
        
        orderedproducts_cnt = orderedproducts.count()
        first_product = OrderProduct.objects.filter(pk__in=id_list,product__vendor=get_vendor_list(request)).first()
        for x in id_list:
                OrderProduct.objects.filter(pk=int(x)).update(status="Packed",updated_at=Now())
                orderproduct = OrderProduct.objects.get(pk=int(x))
                Order.objects.filter(id=orderproduct.order.id,is_ordered=True).update(status="Packed",updated_at=Now())
        
        total = 0
        tax = 0
        grand_total = 0
        temp_total = 0
        if orderedproducts_cnt > 1 :
                for cart_item in orderedproducts:
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

                    #generate pdf
                data = {
                        'ordered_products':orderedproducts,
                        'first_product' : first_product,
                        'total' : total,
                            }
                pdf = render_to_pdf('vendor/pdf_template.html', data)

                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Invoice_%s.pdf" + Now()
                content = "attachment; filename='%s'" %(filename)
                response['Content-Dispositio'] = content 
                
                return response
        else:
            Order.objects.filter(id=orderproduct.order.id,is_ordered=True).update(status="Packed",updated_at=Now())
            OrderProduct.objects.filter(pk__in=id_list,product__vendor=get_vendor_list(request)).update(status="Packed",updated_at=Now())

            first_product = OrderProduct.objects.get(pk__in=id_list,product__vendor=get_vendor_list(request))

            if first_product.variant :
                    price = first_product.variant.variant_price
                    discount = first_product.variant.variant_discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            else:
                    price = first_product.product.price
                    discount = first_product.product.discount
                    temp_total = (sellprice(price,discount) * first_product.quantity)
            total = round(temp_total,2)
            
            data = {
                # 'order' : order,
                'ordered_products':orderedproducts,
                'first_product' : first_product,
                'total' : total,
            }

            pdf = render_to_pdf('vendor/pdf_template.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
    
  
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def readytoship(request,order_number,id):
    pickdate = Now() + datetime.timedelta(days=2) 
    OrderProduct.objects.filter(pk=int(id),product__vendor=get_vendor_list(request)).update(status="ReadyToShip",updated_at=Now())
    Order.objects.filter(order_number=order_number,is_ordered=True).update(status="ReadyToShip",updated_at=Now())
    order = Order.objects.get(order_number=order_number,is_ordered=True)
    Shipping.objects.filter(order_id=order.id,vendor=get_vendor_list(request),is_ordered=True).update(pickup_date=pickdate,updated_at=Now())
    return redirect('vendor_my_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def mass_readytoship(request):
    if request.method == 'POST':
        pickdate = Now() + datetime.timedelta(days=2) 
        id_list = request.POST.getlist('readyboxes')
        
        for x in id_list:
            OrderProduct.objects.filter(pk=int(x),product__vendor=get_vendor_list(request)).update(status="ReadyToShip",updated_at=Now())
            orderproduct = OrderProduct.objects.get(pk=int(x),product__vendor=get_vendor_list(request))
            Order.objects.filter(order_number=orderproduct.order.order_number,is_ordered=True).update(status="ReadyToShip",updated_at=Now())
            Shipping.objects.filter(order_id=orderproduct.order.id,vendor=get_vendor_list(request),is_ordered=True).update(pickup_date=pickdate,updated_at=Now())
    return redirect('vendor_my_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def item_shipped(request,order_number,id):
    OrderProduct.objects.filter(pk=int(id),product__vendor=get_vendor_list(request)).update(status="PickedUpToDeliver",updated_at=Now())
    Order.objects.filter(order_number=order_number,is_ordered=True).update(status="PickedUpToDeliver",updated_at=Now())
    return redirect('vendor_my_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def shipped_in_bulk(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('readyhandover')
   
        for x in id_list:
            OrderProduct.objects.filter(pk=int(x),product__vendor=get_vendor_list(request)).update(status="PickedUpToDeliver",updated_at=Now())
            orderproduct = OrderProduct.objects.get(pk=int(x),product__vendor=get_vendor_list(request))
            Order.objects.filter(order_number=orderproduct.order.order_number,is_ordered=True).update(status="PickedUpToDeliver",updated_at=Now())
    return redirect('vendor_my_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def cancel_item_vendor(request,order_number,id):
    vendor = Vendor.objects.get(user=request.user)
    cancel_reason = request.POST.get('cancel_reason')
    order = Order.objects.get(order_number=order_number,is_ordered=True)
   

    orderlist = []
      

    OrderProduct.objects.filter(pk=id,product__vendor=get_vendor_list(request),order_id=order.id).update(status="Cancelled Item",completed_date=Now(),is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
    
    v_id = []
    data = json.loads(order.total_data)
    for vendor_id in data :
        v_id.append(vendor_id)
    if len(v_id)<2 :
        product_count = OrderProduct.objects.filter(order_id=order.id,vendor=vendor).count()
        cancelled_count = OrderProduct.objects.filter(order_id=order.id,status__contains="Cancelled",vendor=vendor).count()
        if cancelled_count == product_count :
             Order.objects.filter(order_number=order_number,is_ordered=True).update(status="Cancelled Order",is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
             OrderProduct.objects.filter(order_id=order.id).update(status="Cancelled Order",completed_date=Now(),is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
    
    return redirect('vendorder_cancellation')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def request_extension(request,order_number,id):
    days = request.POST.get('ext_days')
  
    order = Order.objects.get(order_number=order_number,is_ordered=True)

    orderproduct = OrderProduct.objects.get(pk=id,product__vendor=get_vendor_list(request),order_id=order.id)
    if orderproduct.SLA_Extension :
         messages.error(request, "SLA extension is already provided")
         return redirect('vendor_my_orders')
    else:
         OrderProduct.objects.filter(pk=id,product__vendor=get_vendor_list(request),order_id=order.id).update(SLA_Extension=days,sla_ext_date=Now())
    return redirect('vendor_my_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def orders_overview(request):
    pass
    
    vendor = Vendor.objects.get(user=request.user)
    # order = Order.objects.filter(vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
 
    orderproducts = OrderProduct.objects.filter(vendor_id=vendor.id).order_by('-created_at')
    orderproducts_toship = OrderProduct.objects.filter(vendor_id=vendor.id,status__in=["Packed","New"]).order_by('-updated_at')#to_ship
    orderproducts_shipped = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="PickedUpToDeliver").order_by('-updated_at') #shipped
    orderproducts_delivered = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="Delivered").order_by('-updated_at') #Delivered
    orderproducts_completed = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="Completed").order_by('-updated_at') #Completed
    orderproducts_cancelled = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="Cancelled").order_by('-updated_at') #Cancellation
    orderproducts_returned = OrderProduct.objects.filter(vendor_id=vendor.id,status__contains="Return").order_by('-updated_at') #Return refund

    list_status = ["Return Approved","Return in Process","Return Request Cancelled","Return Requested"]

    paginator = Paginator(orderproducts,10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

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
        'orderproducts' : paged_orders,
        'orderproducts_toship'	:	paged_orders_toship,
        'orderproducts_shipped'	:	paged_orders_shipped,
        'orderproducts_delivered'	:	paged_orders_delivered,
        'orderproducts_completed'	:	paged_orders_completed,
        'orderproducts_cancelled'	:	paged_orders_cancelled,
        'orderproducts_returned'	:	paged_orders_returned,
        'list_status' : list_status,
    }

    return render(request, 'vendor/order_overview.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def cancel_order_vendor(request,order_number):
    cancel_reason = request.POST.get('cancel_reason')
    Order.objects.filter(order_number=order_number,is_ordered=True).update(status="Cancelled Order",is_cancelled=True,cancellation_reason=cancel_reason,updated_at=Now())
    OrderProduct.objects.filter(order__order_number = order_number,vendor=get_vendor(request)).update(status="Cancelled Order",is_cancelled=True,completed_date=Now(),cancellation_reason=cancel_reason,updated_at=Now())
    order = Order.objects.get(order_number=order_number,is_ordered=True)
   
    return render(request,'vendor/cancellation.html')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorder_cancellation(request):
    vendor = Vendor.objects.get(user=request.user)
    # orders = Order.objects.filter(vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
    orderstemp = Order.objects.filter(is_ordered=True,status__in=('New','Packed')).order_by('-created_at')
    orderproducts = OrderProduct.objects.filter(vendor=vendor,status__in=('New','Packed')).order_by('-created_at')
    orderlist = []
    for order in orderstemp:
        v_id = []
        data = json.loads(order.total_data)
        for vendor_id in data :
             v_id.append(vendor_id)
        if len(v_id)<2:
            orderlist.append(order.order_number)

    orders = Order.objects.filter(order_number__in=orderlist,vendors__in=[vendor.id],is_ordered=True,status__in=('New','Packed')).order_by('-created_at')      


    context={
        'orders' : orders,
        'orders_count' : orders.count(),
        'orderproducts' : orderproducts,

    }
    return render(request,'vendor/cancellation.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def return_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    disputform = DisputeImage_Form()
    refund_all = Refund.objects.filter(vendor_id=vendor.id).order_by('-updated_at')
    return_requested = Refund.objects.filter(vendor_id=vendor.id,return_status="Return Requested")
    return_responded = Refund.objects.filter(vendor_id=vendor.id,return_status__in=["ReadyToProcess","Evidence Submitted"]).order_by('-updated_at')
    
    all_inner_requests = Refund.objects.filter(vendor_id=vendor.id).order_by('-updated_at')
    inner_new_request = Refund.objects.filter(vendor_id=vendor.id,return_status__in=["Return Requested","Return Approved"]).order_by('-updated_at')
    inner_negotiation_pending = Refund.objects.filter(vendor_id=vendor.id,return_status__in=["Continue Return","Countered Offer","Customer Accepted Seller Proposal"]).order_by('-updated_at')
    inner_evidence_requested = Refund.objects.filter(vendor_id=vendor.id,return_status__in=["Seller Dispute"]).order_by('-updated_at')
    inner_validation_progress = Refund.objects.filter(vendor_id=vendor.id,return_status__in=["Return Delivered","Return ReadyToShip"]).order_by('-updated_at')


    paginator = Paginator(refund_all,10)
    page_all = request.GET.get('page')
    page_refund_all = paginator.get_page(page_all)
    
    # tohsip
    paginator = Paginator(return_requested,10)
    page_requested= request.GET.get('page')
    page_return_requested = paginator.get_page(page_requested)

    paginator = Paginator(return_responded,10)
    page_responded = request.GET.get('page')
    page_return_responded = paginator.get_page(page_responded)
    
    # tohsip
    paginator = Paginator(all_inner_requests,10)
    page_inner_requests= request.GET.get('page')
    page_all_inner_requests = paginator.get_page(page_inner_requests)

    paginator = Paginator(inner_new_request,10)
    page_new_request = request.GET.get('page')
    page_inner_new_request = paginator.get_page(page_new_request)
    
    # tohsip
    paginator = Paginator(inner_negotiation_pending,10)
    page_negotiation_pending= request.GET.get('page')
    page_inner_negotiation_pending = paginator.get_page(page_negotiation_pending)

    paginator = Paginator(inner_evidence_requested,10)
    page_evidence_requested = request.GET.get('page')
    page_inner_evidence_requested = paginator.get_page(page_evidence_requested)
    
    # tohsip
    paginator = Paginator(inner_validation_progress,10)
    page_validation_progress= request.GET.get('page')
    page_inner_validation_progress = paginator.get_page(page_validation_progress)

    list_status = ['Return/Refund','Return Requested']
    context={
        'list_status' : list_status,
        'refund_all' : page_refund_all,
        'return_requested' : page_return_requested,
        'return_responded' : page_return_responded,
        'all_inner_requests' : page_all_inner_requests,
        'inner_new_request' : page_inner_new_request,
        'inner_negotiation_pending' :page_inner_negotiation_pending,
        'inner_evidence_requested' :page_inner_evidence_requested,
        'inner_validation_progress' :page_inner_validation_progress,
        'disputform' : disputform,
    }

    return render(request,'vendor/return/return_orders.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def approve_return(request,id):
    Refund.objects.filter(pk=id).update(return_status='Return Approved',buyer_return_status='Return Approved', updated_at=Now())
    refund = Refund.objects.get(pk=int(id))
    OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return Approved",updated_at=Now())
    messages.success(request,f"Refund/Return request is approved, You can offer partial refund from (To Respond - New Request Tab) or ask customer to return product.")
    return redirect('return_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def return_partial_amount(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)

    partialamount = request.POST.get('rpamount')

    if partialamount == '':
        messages.error(request,'Partial amount field must not be empty, please enter partial amount and submit.')
        return redirect('return_orders')
    partialamt = float(partialamount)
    if partialamt > round(orderproduct.product_price * orderproduct.quantity,2) :
              messages.error(request,'Partial offered amount should be less then item price')
              return redirect('return_orders')
    if refund.partial_offer_cnt >=3 :
              messages.error(request,'You can only offer 3 partial amount')
              return redirect('return_orders')
    
    refund.return_status='Partial Refund Offered'
    refund.buyer_return_status='Partial Refund Offered'
    refund.partial_offer_amount = partialamt
    refund.updated_at = Now()
    refund.partial_offer_cnt += 1
    refund.save()
    messages.info(request,"Partial refund is offered, Please wait for reply from customer.")
    return redirect('return_orders')  
@user_passes_test(check_role_vendor)
def return_seller_accept_proposal(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    #Seller accepted buyer's proposal and case will be ready to process the refund
    refund.return_status='ReadyToProcess'
    refund.completed_date = Now()
    refund.refund_title='Seller accepted proposal of Buyer'
    refund.buyer_return_status='Return In Process'
    refund.buyer_payment = refund.counter_amount
    refund.seller_payment = round(refund.total_product_amount - refund.counter_amount,2)
    refund.updated_at = Now()
    refund.save()

    messages.success(request, "Refund amount will be transfered to Buyer account within a week.")
    
    return redirect('return_orders')  

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def close_window_selr(request):
    return redirect('return_orders')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def return_full_refund(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    #Seller accepted to provide full refund
    try:
        if request.method == "POST":
            refund.return_status='ReadyToProcess'
            refund.completed_date = Now()
            refund.refund_title='Seller accepted to provide full refund, buyer returned the item'
            refund.buyer_return_status='Return In Process'
            refund.buyer_payment = refund.total_product_amount
            refund.seller_payment = 0
            refund.updated_at = Now()
            refund.save()

            messages.success(request, "Refund amount will be transfered to Buyer account within a week.")
    except Exception as e:
         print(f'exception occured,{e}')
         messages.error(request, "exception raised")
    return redirect('return_orders')  


def full_refund_noreturn(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    #Seller accepted to provide full refund
    try:
        if request.method == "POST":
            refund.return_status='ReadyToProcess'
            refund.completed_date = Now()
            refund.refund_title='Seller accepted to provide full refund, buyer will not return the item'
            refund.buyer_return_status='Return In Process'
            refund.buyer_payment = refund.total_product_amount
            refund.seller_payment = 0
            refund.updated_at = Now()
            refund.save()

            messages.success(request, "Refund amount will be transfered to Buyer account within a week.")
    except Exception as e:
         print(f'exception occured,{e}')
         messages.error(request, "exception raised")
    return redirect('return_orders') 


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def approvalof_seller_proposal_acceped(request,id):
    refund = Refund.objects.get(pk=int(id))
    orderproduct = OrderProduct.objects.get(id=refund.orderproduct.id)
    #Buyer accepted seller's proposal and case will be ready to process the refund
    try:
        if request.method == "POST":
            refund.return_status='ReadyToProcess'
            refund.completed_date = Now()
            refund.refund_title='Buyer accepted proposal of Seller'
            refund.buyer_return_status='Return In Process'
            refund.buyer_payment = refund.partial_offer_amount
            refund.seller_payment = round(refund.total_product_amount - refund.partial_offer_amount,2)
            refund.updated_at = Now()
            refund.save()

            
            messages.success(request, "Refund amount will be transfered to Buyer account within a week.")
    except Exception as e:
         print(f'exception occured,{e}')
         messages.error(request, "exception raised")
    return redirect('return_orders')  


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def seller_dispute(request,id):
    refund = Refund.objects.get(pk=int(id))
    
    if request.method == "POST":
        dispute_reason = request.POST.get('dispute_reason')
        description = request.POST.get('description')

        ReturnDispute.objects.create(refund = refund,
                                       dispute_reason=dispute_reason,
                                       description=description)
        messages.success(request,"Dispute raised successfully, please submite supperting evidence from Evidence Requested Tab")
    
    
    #Buyer accepted seller's proposal and case will be ready to process the refund
    if dispute_reason == 'We didn\'t receive the return product' :
        refund.return_status='Return Not Delivered'
        refund.buyer_return_status='Return Not Delivered'
    else:
        refund.return_status='Seller Dispute'
        refund.buyer_return_status='Return In Process'
    refund.updated_at = Now()
    refund.save()
    return redirect('return_orders')  

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def upload_evidence_backup(request,id):
    refund = Refund.objects.get(pk=int(id))
    
    if request.method == "POST":
            disputform = DisputeImage_Form(request.POST, request.FILES)
            # image = request.POST.get('images')
            # videofile = request.POST.get('videofile')
           
            if disputform.is_valid():
                try:
                        videopod = disputform.cleaned_data['videopod']
                        videofile = disputform.cleaned_data['videofile']

                        videopodsize = videopod.size
                        videofilesize = videofile.size
                        if videopodsize > 10000000 or videofilesize > 10000000 :
                            messages.error(request, "filesize is 10 MB")
                            return redirect('return_orders')
                        else:

                            files = request.FILES.getlist("images")
                            dispute = disputform.save(commit=False)
                            dispute.refund = refund
                            dispute.save()
                except:
                        messages.error(request, 'File size should not be more then 10 MB')
                        return redirect('return_orders')  
                for i in files:
                        DisputeImages.objects.update(refund=refund, image=i)
                        Refund.objects.filter(pk=id).update(return_status = 'Evidence Submitted',returned_item_toseller=True,buyer_return_status='Return in Process',updated_at = Now())
                        messages.info(request, "Evidence uploaded successfully")
                        return redirect('return_orders') 
           
            else:
                 print(disputform.errors)
                 return redirect('return_orders') 
         
    return redirect('return_orders')   
            
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def upload_evidence(request,id):
    refund = Refund.objects.get(pk=int(id))
    returndispute = ReturnDispute.objects.get(refund=refund)
    if request.method == "POST":
            disputform = DisputeImage_Form(request.POST, request.FILES)
            
           
            if disputform.is_valid():
                videopod = disputform.cleaned_data['videopod']
                videofile = disputform.cleaned_data['videofile']
                returndispute.videofile = videofile
                returndispute.videopod = videopod
                returndispute.save()

                files = request.FILES.getlist("images")

                accept = ['image/jpg','image/jpeg','image/png']
                try:
                    for i in files:
                        
                        file_mime_type = magic.from_buffer(i.read(1024),mime=True)
                        print(file_mime_type)
                        if file_mime_type not in accept:
                            messages.info(request, "Unsupported file type, allowed file types are :jpg,jpeg,png. ")
                            return redirect('return_orders') 
                        else:
                            DisputeImages.objects.create(refund=refund, image=i)
                    messages.info(request, "Evidence uploaded successfully")
                except :
                    messages.info(request, "Unsupported file type, allowed file types are :jpg,jpeg,png. ")
                    return redirect('return_orders')  
               
                Refund.objects.filter(pk=id).update(return_status = 'Evidence Submitted',buyer_return_status='Return in Process',returned_item_toseller=True,updated_at = Now())
                
                
           
            else:
                 messages.error(request, 'File size should not be more then 10 MB')
                 return redirect('upload_evidence',id) 
    else:
          disputform =  DisputeImage_Form()  
    # context = {
    #      'disputform' : disputform,
    # }
         
    return redirect('return_orders')  
    #  return render(request,'vendor/return/upload_evidence.html',context)  

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def reject_straight(request,id):
    refund = Refund.objects.get(pk=int(id))
    if request.method == "POST":
            disputform = DisputeImage_Form(request.POST, request.FILES)
            
           
            if disputform.is_valid():
                dispute_reason = request.POST.get('dispute_reason')
                description = request.POST.get('description')

                videopod = disputform.cleaned_data['videopod']
                videofile = disputform.cleaned_data['videofile']

                ReturnDispute.objects.create(refund = refund,
                                       dispute_reason=dispute_reason,
                                       description=description,
                                       videofile = videofile,
                                       videopod = videopod)

                files = request.FILES.getlist("images")

                accept = ['image/jpg','image/jpeg','image/png']
                try:
                    for i in files:
                        
                        file_mime_type = magic.from_buffer(i.read(1024),mime=True)
                        print(file_mime_type)
                        if file_mime_type not in accept:
                            messages.info(request, "Unsupported file type, allowed file types are :jpg,jpeg,png.")
                            return redirect('return_orders') 
                        else:
                            DisputeImages.objects.create(refund=refund, image=i)
                    messages.info(request, "Evidence uploaded successfully")
                except :
                    messages.info(request, "Unsupported file type, allowed files are :jpg,jpeg,png. ")
                    return redirect('return_orders')  
               
                Refund.objects.filter(pk=id).update(return_status = 'Reject Evidence Submitted',buyer_return_status='Return in Process',updated_at = Now())
                
                
           
            else:
                 messages.error(request, 'File size should not be more then 10 MB')
                 return redirect('reject_straight',id) 
    else:
          disputform =  DisputeImage_Form()  
    # context = {
    #      'disputform' : disputform,
    # }
         
    return redirect('return_orders')  


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_my_returns(request):
    vendor = Vendor.objects.get(user=request.user)
   
    return_all = Refund.objects.filter(vendor_id=vendor.id).order_by('-updated_at')
    return_approved = Refund.objects.filter(vendor_id=vendor.id,return_status="Return Back To Buyer").order_by('-updated_at') #Return refund

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
    }
    return render(request, 'vendor/return/my_returns.html',context)


class returnback_check_mychecklist(View):
    def get(self,request,*args,**kwargs):
        #print all products with invoice
        id_list = request.GET.getlist('boxes')
        returnback_pickup_date = request.GET.get('returnback_pickup_date')

        order_cnt = Refund.objects.filter(pk__in=id_list).aggregate(order_cnt = Count('order_id', distinct=True))["order_cnt"]
        
        if order_cnt > 1:
            messages.error(request,'Please select items belogs to one order at a time to download print label')
            return redirect('vendor_my_returns')
        refund_main = Refund.objects.filter(pk__in=id_list)
        refund_main_cnt = refund_main.count()
        first_product = Refund.objects.filter(pk__in=id_list).first()
        
        for x in id_list:
                if Refund.objects.filter(pk=int(x),return_status="Return Back ReadyToShip").exists():
                     pass
                else:
                    Refund.objects.filter(pk=int(x)).update(return_status="Return Back ReadyToShip",completed_date = Now(),returned_item_tobuyer = True, buyer_return_status='Return in Process',returnback_pickup_date=returnback_pickup_date,updated_at=Now())
                    refund = Refund.objects.get(pk=int(x))
                    order = Order.objects.get(id = refund.order.id)
                    OrderProduct.objects.filter(id=refund.orderproduct.id).update(status="Return in Process",updated_at=Now())
                    
                    if Return_Shipping.objects.filter(order=refund.order, vendor=refund.vendor).exists() :
                        return_shipping = Return_Shipping.objects.get(order=refund.order, vendor=refund.vendor)
                    else:
                        return_shipping = Return_Shipping()
                    
                    return_shipping.order_id = refund.order.id     
                    return_shipping.vendor_id = refund.vendor_id


                    return_shipping.receiver_name = order.full_name			
                    return_shipping.receiver_contact =	order.phone		
                    return_shipping.receiver_email	= order.user.email	
                    return_shipping.receiver_unit = order.unit_no		
                    return_shipping.receiver_postcode = order.pin_code
                    return_shipping.returnback_pickup_date = refund.returnback_pickup_date
                        

                    return_shipping.sender_name =	refund.vendor.vendor_name					
                    return_shipping.sender_contact = refund.vendor.user.phone_number	
                    return_shipping.sender_email =	refund.vendor.user.email	
                    return_shipping.sender_unit = refund.vendor.user.userprofile.unit_no	
                    return_shipping.sender_postcode = refund.vendor.user.userprofile.pin_code	
                    
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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)     
def vendor_maincategory(request):
     vendor = Vendor.objects.get(user=request.user)
     main_categories = Vendor_Main_Category.objects.filter(vendor=vendor).order_by('created_at')
     context={
          'main_categories' : main_categories
     }
     return render(request,'vendor/vendor_maincategory.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)     
def vendor_cat(request):
     vendor = Vendor.objects.get(user=request.user)
     categories = Vendor_Category.objects.filter(vendor=vendor).order_by('created_at')
     context={
          'categories' : categories
     }
     return render(request,'vendor/vendor_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)     
def vendor_subcategory(request):
     vendor = Vendor.objects.get(user=request.user)
     sub_categories = Vendor_Sub_Category.objects.filter(vendor=vendor).order_by('created_at')
     context={
          'sub_categories' : sub_categories 
     }
     return render(request,'vendor/vendor_subcategory.html',context)
     
def products_by_maincategory(request,pk):
     vendor = Vendor.objects.get(user=request.user)
     maincat = Vendor_Main_Category.objects.get(vendor=vendor,pk=pk)
     main_category = Main_Category.objects.get(name=maincat)

     products = Product.objects.filter(vendor=vendor, main_category=main_category).order_by('-id')
     product_count = products.count()
     context={
          'products' : products,
          'product_count' :product_count,
     }
     return render(request, 'vendor/products_by_maincategory.html',context)


def products_by_cat(request,pk):
    vendor = Vendor.objects.get(user=request.user)
    cat = Vendor_Category.objects.get(vendor=vendor,pk=pk)
    category = Category.objects.filter(name=cat)
    products = Product.objects.filter(vendor=vendor, category__in=category).order_by('-id')
    product_count = products.count()
    context={
          'products' : products,
          'product_count' :product_count,
     }
    return render(request, 'vendor/products_by_category.html',context)


def products_by_subcategory(request,pk):
    vendor = Vendor.objects.get(user=request.user)
    sub_cat=Vendor_Sub_Category.objects.get(vendor=vendor,id=pk)

    sub_category = Sub_Category.objects.filter(name=sub_cat.name)
    print('sub category details are :',sub_category)
    products = Product.objects.filter(sub_category__in=sub_category)

    product_count = products.count()
    context={
          'products' : products,
          'product_count' :product_count,
     }
    return render(request, 'vendor/products_by_subcategory.html',context)

def add_main_category(request):
     if request.method == 'POST':
        form = MainCategoryForm(request.POST)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Main category added syuccessfully")
             return redirect("vendor_maincategory")
     else:
          form = MainCategoryForm()
     context = {
          'form' : form
     }
     return render(request, 'vendor/add_main_category.html',context)

def edit_main_category(request,pk):
     main_category = get_object_or_404(Vendor_Main_Category,pk=pk)
     if request.method == 'POST':
        form = MainCategoryForm(request.POST, instance=main_category)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Main category updated syuccessfully")
             return redirect("vendor_maincategory")
        else:
             print(form.errors)
     else:
          form = MainCategoryForm(instance=main_category)
     context = {
          'form' : form,
          'main_category' : main_category,
     }
     return render(request, 'vendor/edit_main_category.html',context)

def delete_main_category(request,pk):
    main_category = get_object_or_404(Vendor_Main_Category,pk=pk)
    main_category.delete()
    messages.success(request,'Main Category has been deleted successfully')
    return redirect('vendor_maincategory')


def add_category(request):
     if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Category added syuccessfully")
             return redirect("vendor_cat")
        else:
             print(form.errors)
     else:
          form = CategoryForm()
     context = {
          'form' : form
     }
     return render(request, 'vendor/add_category.html',context)

def edit_category(request,pk):
     category = get_object_or_404(Vendor_Category,pk=pk)
     if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Category updated syuccessfully")
             return redirect("vendor_cat")
        else:
             print(form.errors)
     else:
          form = CategoryForm(instance=category)
     context = {
          'form' : form,
          'category' : category,
     }
     return render(request, 'vendor/edit_category.html',context)

def delete_category(request,pk):
    category = get_object_or_404(Vendor_Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully')
    return redirect('vendor_cat')




def add_sub_category(request):
     if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Sub category added syuccessfully")
             return redirect("vendor_subcategory")
        else:
             print(form.errors)
     else:
          form = SubCategoryForm()
     context = {
          'form' : form
     }
     return render(request, 'vendor/add_sub_category.html',context)

def edit_sub_category(request,pk):
     sub_category = get_object_or_404(Vendor_Sub_Category,pk=pk)
     if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=sub_category)
        if form.is_valid():
             name = form.cleaned_data['name']
             category=form.save(commit=False)
             category.vendor = get_vendor(request)
             category.slug = slugify(name)
             category.save()
             messages.success(request,"Sub category updated syuccessfully")
             return redirect("vendor_subcategory")
        else:
             print(form.errors)
     else:
          form = SubCategoryForm(instance=sub_category)
     context = {
          'form' : form,
          'sub_category' : sub_category,
     }
     return render(request, 'vendor/edit_sub_category.html',context)

def delete_sub_category(request,pk):
    category = get_object_or_404(Vendor_Sub_Category,pk=pk)
    category.delete()
    messages.success(request,'Sub category has been deleted successfully')
    return redirect('vendor_subcategory')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vend_category_module(request):
    form = SubCategoryForm(request.GET)

    return HttpResponse(form['category'])

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_balance(request):
    return render(request,'vendor/my_balance.html')

