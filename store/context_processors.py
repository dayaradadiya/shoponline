from app.models import Brand
from store.models import Product, Size, Variants
from django.db.models import Min,Max

# def get_filters(request):
    
#     products = Product.objects.all().filter(is_available=True).order_by('created_date')
#     color=Variants.objects.filter(product__id__in=products).values('color__id','color__code','color__name').distinct()
#     size=Size.objects.all().distinct()
#     brand = Brand.objects.all().distinct()
#     minMaxPrice = Product.objects.all().aggregate(Min('price'),Max('price'))

#     context = {
#         'color' : color,
#         'size' : size,
#         'brand' : brand,
#         'minMaxPrice' : minMaxPrice,
#     }