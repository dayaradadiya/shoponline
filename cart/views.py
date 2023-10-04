from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from cart.forms import ShopCartForm
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from orders.forms import OrderForm
from store.models import Product, Variation
from  django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def sellprice(price,discount):
    discount = float(discount)
    price = float(price)
    if  discount == 0:
        return price
    sellprice = price
    sellprice = round(price - (sellprice * discount/100),2)
    return sellprice
  

def add_cart(request,product_id):
    current_user= request.user
    product = Product.objects.get(id=product_id) #get product
    variantid=None
    if current_user.is_authenticated:
        if product.variant != 'None':
            variantid = request.POST.get('variantid')  # from variant add to cart
            checkinvariant = CartItem.objects.filter(variant_id=variantid, user=current_user)  # Check product in shopcart
            if checkinvariant:
                control = 1 # The product is in the cart
            else:
                control = 0 # The product is not in the cart"""
        else:
            
            checkinproduct = CartItem.objects.filter(product_id=product_id, user=current_user) # Check product in shopcart
            if checkinproduct:
                control = 1 # The product is in the cart
            else:
                control = 0 # The product is not in the cart"""

        if request.method == 'POST':  # if there is a post
            form = ShopCartForm(request.POST)
            if form.is_valid():
                if control==1: # Update  shopcart
                    if product.variant == 'None':
                        data = CartItem.objects.get(product_id=product_id, user_id=current_user.id)
                    else:
                        data = CartItem.objects.get(product_id=product_id, variant_id=variantid, user_id=current_user.id)
                    # data.quantity += form.cleaned_data['quantity']
                    data.quantity = form.cleaned_data['quantity']
                    data.vendor_id = product.vendor.id
                    data.save()  # save data
                else : # Inser to Shopcart
                    data = CartItem()
                    data.user_id = current_user.id
                    data.product_id = product_id
                    data.vendor = product.vendor
                    data.variant_id = variantid
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
            messages.success(request, "Product added to Shopcart ")
            return redirect('cart')

        else: # if there is no post
            if control == 1:  # Update  shopcart
                data = CartItem.objects.get(product_id=product_id, user_id=current_user.id)
                data.quantity += 1
                data.save()  #
            else:  #  Insert to Shopcart
                data = CartItem()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.product_id = product_id
                data.vendor = product.vendor
                data.quantity = 1
                data.variant_id =None
                data.save()  #
            messages.success(request, "Product added to Shopcart")
            return redirect('cart')
    else:
         try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using present session
         except Cart.DoesNotExist :
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
         cart.save()
         if product.variant != 'None':
            variantid = request.POST.get('variantid')  # from variant add to cart
            checkinvariant = CartItem.objects.filter(variant_id=variantid, cart=cart)  # Check product in shopcart
            if checkinvariant:
                control = 1 # The product is in the cart
            else:
                control = 0 # The product is not in the cart"""
         else:
            checkinproduct = CartItem.objects.filter(product_id=product_id, cart=cart) # Check product in shopcart
            if checkinproduct:
                control = 1 # The product is in the cart
            else:
                control = 0 # The product is not in the cart"""

         if request.method == 'POST':  # if there is a post
            form = ShopCartForm(request.POST)
            if form.is_valid():
                if control==1: # Update  shopcart
                    if product.variant == 'None':
                        data = CartItem.objects.get(product_id=product_id, cart=cart)
                    else:
                        data = CartItem.objects.get(product_id=product_id, variant_id=variantid, cart=cart)
                    # data.quantity += form.cleaned_data['quantity']
                    data.quantity = form.cleaned_data['quantity']
                    data.vendor = product.vendor
                    data.save()  # save data
                else : # Inser to Shopcart
                    data = CartItem()
                    data.cart = cart
                    data.product_id = product_id
                    data.vendor = product.vendor
                    data.variant_id = variantid
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
            messages.success(request, "Product added to Shopcart ")
            return redirect('cart')

         else: # if there is no post
            if control == 1:  # Update  shopcart
                data = CartItem.objects.get(product_id=product_id, cart=cart)
                data.quantity += 1
                data.vendor = product.vendor
                data.save()  #
            else:  #  Inser to Shopcart
                data = CartItem()  # model ile bağlantı kur
                data.cart = cart
                data.product_id = product_id
                data.quantity = 1
                data.variant_id =None
                data.vendor = product.vendor
                data.save()  #
            messages.success(request, "Product added to Shopcart")
            return redirect('cart')
         





def cart(request, total=0, quantity=0,cart_items=None):
   
    try:
        tax = 0
        grand_total = 0
        temp_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True).order_by('created_at')
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
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'grand_total' : grand_total,
        'tax' : tax,
    }

    return render(request, 'store/cart.html',context)

def remove_cart(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -=1
            if cart_item.quantity < cart_item.product.min_order_quantity:
                cart_item.quantity +=1
                messages.error(request, "you cannot order lesser then minimum allowed quantity")
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')




            
def get_max_qty(max_allowed_quantity,stock):
                if stock < max_allowed_quantity:
                     return  stock 
                else :
                      return  max_allowed_quantity  

def add_cart_button(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 0 :
            cart_item.quantity +=1
            if cart_item.variant:
                max_qty = get_max_qty(cart_item.variant.variant_max_allowed_quantity, cart_item.variant.variant_stock)
            else:
                max_qty = get_max_qty(cart_item.product.max_allowed_quantity, cart_item.product.stock)
            if max_qty < cart_item.quantity:
                messages.error(request, "you have exceeded limit of maximum allowed quantity")
                cart_item.quantity = max_qty
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')




def remove_cart_item(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    messages.success(request,'Cart Item is removed successfully')

    return redirect('cart')

# def remove_cart_item(request):
#     product_id=id = request.GET['product_id']
#     cart_item_id = request.GET['cart_item_id']
#     product = get_object_or_404(Product, id=product_id)
    
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
#     cart_item.delete()

#     data ={
#         'status' : 'Deleted successfully',
#         'status_text' : 'Cart Item is removed successfully',
#         'status_icon':'success'
#     }
#     return JsonResponse(data)
