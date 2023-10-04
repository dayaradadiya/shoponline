from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Brand
from cart.context_processors import get_wishlist_counter
from cart.models import CartItem
from category.models import Category, Main_Category, Sub_Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from orders.models import OrderProduct
from .forms import ReviewForm
from django.db.models import Count
from cart.views import _cart_id
from django.db.models import Min,Max
from  django.contrib.auth.decorators import login_required

from django.contrib import messages
from . models import Contact, Images, Product, ProductGallery, ReviewRating, Size, Specification, Variants,  WishlistModel

from tablib import Dataset
from .resources import ProductResource
# Create your views here.


def store(request,category_slug=None):
    categories = None
    products = None

    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "")
    
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')
 

    if category_slug !=None :
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True,is_active=True)
        
        if ordering:
            products = products.order_by(ordering) 

        if price:
            products = products.filter(price__lt = price)
        minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

    

        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True,is_active=True).order_by('id')
        
        if ordering:
            products = products.order_by(ordering) 
        if price:
            products = products.filter(price__lt = price)

        # if price:
        #     products = products.filter(price__lt = price)
        minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
        'min_price':min_price,
        'max_price':max_price,
    }
    return render(request,'store/store.html',context)   

def maincategory_list(request,maincat_id):
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    maincategory=Main_Category.objects.get(id=maincat_id,is_active=True)
    products = Product.objects.filter(main_category = maincategory,is_active=True)

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)

    product_count = products.count()

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
       
    }
    return render(request,'store/store.html',context) 

def category_list(request,cat_id):
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    # category1 = get_object_or_404(Category, id=cat_id)
    category=Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category,is_active=True)
    product_count = products.count()

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)
        
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    

    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
    }
    return render(request,'store/store.html',context) 


def main_category_product_list(request,maincat_id):
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    # category1 = get_object_or_404(Category, id=cat_id)
    maincategory=Main_Category.objects.get(id=maincat_id,is_active=True)
    products = Product.objects.filter(main_category = maincategory,is_active=True)
    product_count = products.count()

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
       
    }
    return render(request,'store/store.html',context) 




def category_product_list(request,cat_id):
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    # category1 = get_object_or_404(Category, id=cat_id)
    category=Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category,is_active=True)
    product_count = products.count()

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)
        
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
    }
    return render(request,'store/store.html',context) 



def sub_category_product_list(request,sub_cat_id):
    ordering = request.GET.get('ordering', "") 
    price = request.GET.get('price', "") 
    # category1 = get_object_or_404(Category, id=cat_id)
    # sub_category = Sub_Category.objects.filter(sub_category=sub_cat_id)
    products = Product.objects.filter(sub_category=sub_cat_id,is_active=True)
    sub_category =  Sub_Category.objects.get(id=sub_cat_id)
    product_count = products.count()

    color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
    size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
    brand = Brand.objects.all().distinct()
    minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

    if ordering:
            products = products.order_by(ordering) 
    if price:
            products = products.filter(price__lt = price)

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products' : paged_products,
        'product_count' : product_count,
        'color' : color,
        'size' : size,
        'brand' : brand,
        'minMaxPrice' : minMaxPrice,
        'sub_category' : sub_category
    }
    return render(request,'store/store.html',context) 

def product_detail(request,category_slug,product_slug):
    try:
        query = request.GET.get('q')
        single_product = Product.objects.get(category__slug=category_slug,slug = product_slug)
        category = Category.objects.all()
        images = Images.objects.filter(product_id = single_product.id)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        products = Product.objects.all().exclude(id=single_product.id)
        related_products = Product.objects.filter(category__slug=category_slug).exclude(id=single_product.id)
        
        
    except Exception as e:
        raise e
    
    if request.user.is_authenticated :
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct= None
    else:
        orderproduct= None  

    #get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id ,status=True)

    #get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)

    #get the product specifications
    if  Specification.objects.filter(product_id = single_product.id).exists():
         product_specn = Specification.objects.get(product_id = single_product.id)
        
    else:
        product_specn='' 

    context = {
        'single_product' : single_product,
        'images' : images,
        'category': category,
        'in_cart' : in_cart,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
        'product_gallery' : product_gallery,
        'product_specn' : product_specn,
        'item' : related_products,
        'products' : products,
    }

    if single_product.variant != "None" : #product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id = single_product.id,size_id = variant.size_id)
            sizes = Variants.objects.raw('select size_id,name,id from (SELECT  size_id FROM store_variants WHERE product_id=%s GROUP BY size_id) t1,(select * from store_size) t2 where t1.size_id = t2.id' ,[single_product.id])
            sizes_all = Variants.objects.raw('select * from store_variants WHERE product_id=%s' ,[single_product.id])
           
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)

        else:
            variants = Variants.objects.filter(product_id=single_product.id)
            colors = Variants.objects.filter(product_id = single_product.id,size_id = variants[0].size_id)
            sizes = Variants.objects.raw('select size_id,name,id from (SELECT  size_id FROM store_variants WHERE product_id=%s GROUP BY size_id) t1,(select * from store_size) t2 where t1.size_id = t2.id' ,[single_product.id])
            sizes_all = Variants.objects.raw('select * from store_variants WHERE product_id=%s' ,[single_product.id])
            variant = Variants.objects.get(id = variants[0].id)
        context.update({
            'sizes' : sizes,
            'colors' : colors,
            'variant' : variant,
            'query' : query,
            'sizes_all' : sizes_all,
        })

    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword),is_active=True)
        product_count = products.count()

        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {'products' : paged_products,'product_count':product_count,}

    return render(request,'store/store.html',context)

def submit_review(request,product_id):
    
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.filter(user__id=request.user.id,product__id = product_id).first()
            form = ReviewForm(request.POST,instance=reviews)
            if form.is_valid():
               

                subject = form.cleaned_data['subject']
                rating = form.cleaned_data['rating']
                review = form.cleaned_data['review']
                pros = form.cleaned_data['pros']
                cons = form.cleaned_data['cons']
                
                reviews.subject = subject
                reviews.rating = rating
                reviews.review = review
                reviews.pros = pros
                reviews.cons = cons

                reviews.save()
                messages.success(request,'Thank you! the review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data= ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.pros = form.cleaned_data['pros']
                data.cons = form.cleaned_data['cons']

                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id 
                data.save()
                messages.success(request,'Thank you! your review has been submitted.')
                return redirect(url)
  
            
def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id = productid, size_id = size_id )

        context = {
            'size_id' : size_id,
            'productid' : productid,
            'colors' : colors,
        }
        t = render_to_string('store/color_list.html', context=context) 
        # data = {'data' : render_to_string('store/color_list.html', context=context) }
        # data = {'rendered_table' : render_to_string('store/color_list.html', context=context) }
    return JsonResponse({'data':t})

def ordertracking(request):
    return render(request, 'orders/tracker.html')
   
def search_man(request):
        ordering = request.GET.get('ordering', "") 
        price = request.GET.get('price', "") 
        sub_category = Sub_Category.objects.filter(name__contains="Man")
        # products = Product.objects.order_by('-created_date').filter(Q(sub_category=sub_category))
        products = Product.objects.filter(sub_category__in=sub_category,is_active=True)
        product_count = products.count()

        color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
        size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
        brand = Brand.objects.all().distinct()
        minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

        if ordering:
            products = products.order_by(ordering) 
        if price:
            products = products.filter(price__lt = price)

        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = { 'products' : paged_products,
                    'product_count':product_count,
                    'color' : color,
                    'size' : size,
                    'brand' : brand,
                    'minMaxPrice' : minMaxPrice,
                   }

        return render(request,'store/store.html',context)

def search_women(request):
        ordering = request.GET.get('ordering', "") 
        price = request.GET.get('price', "")
        sub_category = Sub_Category.objects.filter(name__contains="Women")
        # products = Product.objects.order_by('-created_date').filter(Q(sub_category=sub_category))
        products = Product.objects.filter(sub_category__in=sub_category,is_active=True)
        product_count = products.count()

        color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
        size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
        brand = Brand.objects.all().distinct()
        minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

        if ordering:
            products = products.order_by(ordering) 
        if price:
            products = products.filter(price__lt = price)

        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {'products' : paged_products,
                   'product_count':product_count,
                   'color' : color,
                    'size' : size,
                    'brand' : brand,
                    'minMaxPrice' : minMaxPrice,
                    }

        return render(request,'store/store.html',context)


def search_kids(request):
        ordering = request.GET.get('ordering', "") 
        price = request.GET.get('price', "")
        sub_category = Sub_Category.objects.filter(Q(name__icontains="Girl") | Q(name__icontains="Boy"))
            # products = Product.objects.order_by('-created_date').filter(Q(sub_category=sub_category))
        products = Product.objects.filter(sub_category__in=sub_category,is_active=True)
        product_count = products.count()

        color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
        size=Variants.objects.filter(product__id__in=products).values('size__id','size__name').distinct()
        brand = Brand.objects.all().distinct()
        minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

        if ordering:
            products = products.order_by(ordering) 
        if price:
            products = products.filter(price__lt = price)

        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {'products' : paged_products,
                   'product_count':product_count,
                   'color' : color,
                    'size' : size,
                    'brand' : brand,
                    'minMaxPrice' : minMaxPrice,}

        return render(request,'store/store.html',context)


def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')



    allProducts = Product.objects.all().order_by('-id')

 
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(variants__size__id__in=sizes).distinct()
    if len(colors) > 0:
        allProducts = allProducts.filter(variants__color__id__in=colors).distinct()
    if len(colors)==0  and len(categories)==0 and len(brands)==0 and len(sizes)==0:
        allProducts=Product.objects.all().order_by('-id')
    t=render_to_string('ajax/product-list.html',{'data':allProducts,'product_count':allProducts.count()})
    return JsonResponse({'data':t})

@login_required(login_url='login')
def add_to_wishlist(request):
     product_id = request.GET['id']
     product = Product.objects.get(id=product_id)

     context = {}
     whishlist_count = WishlistModel.objects.filter(product=product,user=request.user).count()

     if whishlist_count > 0 :
          context = {
               "bool" : True
          }
          
     else:
          new_wishlist = WishlistModel.objects.create(
               product=product,
               user=request.user
               )
          context = {
                    "bool" : True,
                    "wishlist_counter" : get_wishlist_counter(request),
                }
          

     return JsonResponse(context)

def help_topics(request):
     return render(request,'store/help_topics.html')





def about(request):
     return render(request, 'store/about.html')

def contactus(request):
     if request.method == 'POST':
          name = request.POST['name']
          email = request.POST['email']
          phone = request.POST['phone']
          content = request.POST['content']
          subject = request.POST['subject']

          contact = Contact(name=name,email=email,phone=phone,content=content,subject=subject)  
          contact.save()
          messages.success(request,"Message sent Successfully !")
          return HttpResponseRedirect('/')
     return render(request, 'store/contactus.html')
     

def ImportExcel(request):
     if request.method == 'POST' :
          product_resource = ProductResource()
          dataset = Dataset()
          new_products = request.Files['my_file']
          imported_data = dataset.load(new_products.read(),format='xlsx')
          for data in imported_data:
               value = Product(
                    data[0],
                    data[1],
                    data[2]
               )
               value.save()
     return render(request,'store/bulkproduct.html')



     