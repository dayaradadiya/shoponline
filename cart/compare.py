from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category, Main_Category, Sub_Category
from django.core.paginator import Page, EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from orders.models import OrderProduct
from .forms import ReviewForm, ShopCartForm
from django.db.models import Count

from django.contrib import messages
from . models import Cart, Images, Product, ProductGallery, ReviewRating, Size, Variants


def add_cart_button(request,product_id):
    current_user= request.user
    product = Product.objects.get(id=product_id) #get product
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
                    data.quantity += 1
                    data.save()  # save data
                else : # Inser to Shopcart
                    data = CartItem()
                    data.user_id = current_user.id
                    data.product_id =product_id
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
            else:  #  Inser to Shopcart
                data = CartItem()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.product_id = product_id
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
                    data.quantity +=1
                    data.save()  # save data
                else : # Inser to Shopcart
                    data = CartItem()
                    data.cart = cart
                    data.product_id = product_id
                    data.variant_id = variantid
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
            messages.success(request, "Product added to Shopcart ")
            return redirect('cart')

         else: # if there is no post
            if control == 1:  # Update  shopcart
                data = CartItem.objects.get(product_id=product_id, cart=cart)
                data.quantity += 1
                data.save()  #
            else:  #  Inser to Shopcart
                data = CartItem()  # model ile bağlantı kur
                data.cart = cart
                data.product_id = product_id
                data.quantity = 1
                data.variant_id =None
                data.save()  #
            messages.success(request, "Product added to Shopcart")
            return redirect('cart')
