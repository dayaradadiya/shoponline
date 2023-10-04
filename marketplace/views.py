from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from category.models import Category, Main_Category, Vendor_Category, Vendor_Main_Category
from store.models import Product
from vendor.models import Vendor
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.core.paginator import Page, EmptyPage,PageNotAnInteger,Paginator
# Create your views here.



def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count,
    }
    return render(request, 'marketplace/listing.html',context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    
    vend_main_category = Vendor_Main_Category.objects.filter(vendor=vendor)

    vendor_category = Vendor_Category.objects.filter(vendor=vendor,main_category__in=vend_main_category)
   
    print('vendor_categories are :',vendor_category)

  

    products = Product.objects.filter(vendor=vendor.id,is_active=True)

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()



    request.session['vendor_slug'] = vendor_slug
    context = {
        'vendor' : vendor,
        'vend_main_category' : vend_main_category,
        'vend_category' : vendor_category,
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request,'marketplace/vendor_detail.html',context)




def vend_main_cat_prod_list(request,maincat_id,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    # category1 = get_object_or_404(Category, id=cat_id)
    maincategory=Vendor_Main_Category.objects.get(vendor=vendor,id=maincat_id)
    main_category = Main_Category.objects.get(name=maincategory)
    products = Product.objects.filter(vendor=vendor,main_category = main_category)
    product_count = products.count()

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    vend_main_category = Vendor_Main_Category.objects.filter(vendor=vendor)

    vendor_category = Vendor_Category.objects.filter(vendor=vendor,main_category__in=vend_main_category)

    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'vend_main_category' : vend_main_category,
        'vendor_category' : vendor_category,
       
    }
    return render(request,'marketplace/vendor_detail.html',context) 



def vend_cat_prod_list(request,cat_id,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    cat=Vendor_Category.objects.get(vendor=vendor,id=cat_id)

    category = Category.objects.filter(name=cat)
    products = Product.objects.filter(vendor=vendor,category__in=category,is_active=True)
    product_count = products.count()

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)
        
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    vend_main_category = Vendor_Main_Category.objects.filter(vendor=vendor)

    vendor_category = Vendor_Category.objects.filter(vendor=vendor,main_category__in=vend_main_category)

    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'vend_main_category' : vend_main_category,
        'vendor_category' : vendor_category,
    }
    return render(request,'marketplace/vendor_detail.html',context) 

