from . import views
from django.urls import include, path

urlpatterns = [
    path('',views.myAccount),
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),

    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),

    path('request_refund/<int:pk>',views.request_refund,name='request_refund'),
    path('request_refund/reason/',views.htmx_reason,name='htmx_reason'),


    path('vendor/',include('vendor.urls')),
    path('customer/',include('customers.urls')),

    path('wishlist_view/',views.wishlist_view,name='wishlist_view'),

    path('remove_wishlist_item/<int:product_id>/<int:item_id>/',views.remove_wishlist_item,name='remove_wishlist_item'),

    path('change_refund_address/<int:itemid>/<int:id>',views.change_refund_address,name='change_refund_address'),

    path('otp',views.otp_view,name='otp'),
    

]