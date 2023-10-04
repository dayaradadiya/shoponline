from . import views
from django.urls import include, path
from accounts import views as AccountViews

urlpatterns = [

    path('',views.admin_login,name='admin_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('generateShipping/',views.generateShipping,name='generateShipping'),
    path('vendor_payout/',views.vendor_payout,name='vendor_payout'),
    path('shop_approval/<int:id>',views.shop_approval,name='shop_approval'),
    path('shop_rejection/<int:id>',views.shop_rejection,name='shop_rejection'),
    path('return_process',views.return_process,name='return_process'),
    path('close_window_admin',views.close_window_admin,name='close_window_admin'), 
    path('generateReturnShipping',views.generateReturnShipping,name='generateReturnShipping'),
    path('return_vendor_payout/',views.return_vendor_payout,name='return_vendor_payout'),
    

]