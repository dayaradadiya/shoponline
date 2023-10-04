from . import views
from django.urls import include, path
from accounts import views as AccountViews

urlpatterns = [
    

    path('',views.marketplace,name='marketplace'),
    path('<slug:vendor_slug>/',views.vendor_detail,name='vendor_detail'),
    path('vend_main_cat_prod_list/<int:maincat_id>/<slug:vendor_slug>',views.vend_main_cat_prod_list,name='vend_main_cat_prod_list'),
    path('vend_cat_prod_list/<int:cat_id>/<slug:vendor_slug>',views.vend_cat_prod_list,name='vend_cat_prod_list'),

    
]