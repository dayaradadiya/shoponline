from cart.views import _cart_id, sellprice
from store.models import WishlistModel
from . models import Cart, CartItem





def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
                tax = 0
                grand_total = 0
                temp_total = 0
                total = 0
                cart = Cart.objects.filter(cart_id=_cart_id(request))
                if request.user.is_authenticated:
                    cart_items_2 = CartItem.objects.all().filter(user=request.user)
                   
                else:
                    cart_items_2 = CartItem.objects.all().filter(cart=cart[:1])
                   
                for cart_item in cart_items_2:
                    if cart_item.variant :
                             temp_total += (sellprice(cart_item.variant.variant_price,cart_item.variant.variant_discount) * cart_item.quantity)
                    else:
                             temp_total += (sellprice(cart_item.product.price,cart_item.product.discount) * cart_item.quantity)
                    cart_count += cart_item.quantity
                    total = round(temp_total,2)
                tax = (0*total)/100
                grand_total = round(tax + total,2)
        except Cart.DoesNotExist:
            cart_count = 0
            grand_total = 0
            total = 0
    context = {
        'cart_count' : cart_count,
        'cart_items_2' : cart_items_2,
        'grand_total' : grand_total,
       
    }
    return context
    # return dict(cart_count=cart_count,)

def get_wishlist_counter(request):
    try:
            if request.user.is_authenticated:
                wishlist = WishlistModel.objects.filter(user=request.user)
                wishlist_count = wishlist.count()
            else:
                wishlist_count = 0 
    except:
          wishlist_count = 0 

    context = {
        'wishlist_count' : wishlist_count
    }
    
    return context