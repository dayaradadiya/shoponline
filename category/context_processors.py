from django.shortcuts import get_object_or_404
from category.models import Category, Main_Category, Sub_Category, Vendor_Category, Vendor_Main_Category
from store.models import Product
from vendor.models import Vendor


def menu_links(request):


    main_category = Main_Category.objects.filter(is_active=True)
    # main_category_firsthalf = Main_Category.objects.filter(is_active=True).order_by('id')[:3]
    # main_category_secondhalf = Main_Category.objects.filter(is_active=True).order_by('id')[3:6]
    
    # first_category = main_category[:1]
    first_category = Main_Category.objects.filter(is_active=True).order_by('id').first()

    exclude_first_main_category = Main_Category.objects.filter(is_active=True).order_by('id')[1:]
    category = Category.objects.filter(main_category=main_category).order_by('id')[:3]
    sub_category = Sub_Category.objects.filter(category = category).order_by('id')[:3]

    clothing_category = Main_Category.objects.filter(is_active=True, name__in=['Women clothes','Men clothes','Baby & kids fashion'])    
    shoe_category = Main_Category.objects.filter(is_active=True, name__in=['Women shoes','Men shoes','Sports & Outdoors'])  
    
    shoe_maincategory = Main_Category.objects.get(is_active=True, name='Baby & kids fashion')
    shoe_subcategory = Category.objects.filter(main_category=shoe_maincategory,name__in=['Girl Shoes','Boy Shoes'])

    hnl_maincategory = Main_Category.objects.get(is_active=True, name='Home & Living')
    hnl_subcategory = Category.objects.filter(main_category=hnl_maincategory,name__in=['Furniture','Decoration','Home Fragrance & Aromatherapy'])

    gadget_maincategory = Main_Category.objects.get(is_active=True, name='Mobile & Gadgets')
    gadget_subcategory = Category.objects.filter(main_category=gadget_maincategory,name__in=['Mobile Phones','Wearable Devices','Accessories'])

    fashion_maincategory = Main_Category.objects.get(is_active=True, name='Fashion accessories')
    fashion_subcategory = Category.objects.filter(main_category=fashion_maincategory,name__in=['Hats & Caps','Belts','Hair Accessories'])

    game_maincategory = Main_Category.objects.filter(is_active=True, name__in = ['Gaming & Consoles', 'Cameras & Drones'])
    game_subcategory = Category.objects.filter(main_category__in=game_maincategory,name__in=['Video Games','Console Machines','Cameras'])

    context = {
        'main_category' : main_category,    
        'category' : category,
        'first_category' : first_category,
        'exclude_first_main_category' : exclude_first_main_category,
        'sub_category' : sub_category,
        'clothing_category' : clothing_category,
        'shoe_category' : shoe_category,
        'shoe_subcategory' :shoe_subcategory,
        'hnl_subcategory' : hnl_subcategory,
        'gadget_subcategory' : gadget_subcategory,
        'fashion_subcategory' : fashion_subcategory,
        'game_subcategory' : game_subcategory,
        # 'main_category_firsthalf' : main_category_firsthalf,
        # 'main_category_secondhalf' : main_category_secondhalf,
    }
    return context


# def category_links(request):
#    context = {}
#    if 'vendor_slug' in request.session:
#             vendor_slug = request.session['vendor_slug']
#             vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
#             vend_main_category = Vendor_Main_Category.objects.filter(vendor=vendor)
#             vendor_category = Vendor_Category.objects.filter(vendor=vendor,main_category__in=vend_main_category)
#             context.update(
#                  {
#                      'vend_main_category' : vend_main_category,
#                      'vend_category' : vendor_category,  
#                  }
#             )
#             return context