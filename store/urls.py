from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('',views.store, name='store'),
    # path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('category_product_list/<int:cat_id>',views.category_product_list,name='category_product_list'),
    path('main_category_product_list/<int:maincat_id>/',views.main_category_product_list,name='main_category_product_list'),
    path('maincategory_list/<int:maincat_id>/',views.maincategory_list,name='maincategory_list'),
    path('category_list/<int:cat_id>/',views.category_list,name='category_list'),
    
    path('product_detail/<slug:category_slug>/<slug:product_slug>',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),

    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),

    path('sub_category_product_list/<int:sub_cat_id>',views.sub_category_product_list,name='sub_category_product_list'),

    path('ajaxcolor/',views.ajaxcolor,name='ajaxcolor'),
    
    path('ordertracking/',views.ordertracking,name='ordertracking'),

    path('search_man/',views.search_man,name='search_man'),

    path('search_women/',views.search_women,name='search_women'),

    path('search_kids/',views.search_kids,name='search_kids'),

    path('filter-data',views.filter_data,name='filter-data'),
    
    path('add-to-wishlist/',views.add_to_wishlist,name='add-to-wishlist'),

    path('help_topics/',views.help_topics,name='help_topics'),

    path('about/',views.about,name='about'),

    path('contactus/',views.contactus,name='contactus'),

    path('import_product/',views.ImportExcel,name='push_product_excel'),

    
   
]