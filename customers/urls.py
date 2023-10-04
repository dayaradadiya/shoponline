from . import views
from django.urls import include, path
from accounts import views as AccountViews

urlpatterns = [
    path('',AccountViews.custDashboard,name='customer'),
    path('profile/',views.cprofile,name='cprofile'),
    path('my_orders/',views.my_orders,name='customer_my_orders'),
    path('order_details/<str:order_number>/',views.order_details,name='customer_order_details'),

    path('address/',views.address,name='customer_address'),
    path('make_address_default/',views.make_address_default,name='make_address_default'),


    path('delete-address/<int:pk>/',views.delete_customer_address,name='delete_customer_address'),
    path('edit_customer_address/<int:pk>/',views.edit_customer_address,name='edit_customer_address'),
    path('cancel_item_customer/<str:order_number>/<int:id>',views.cancel_item_customer,name='cancel_item_customer'),
 
    path('custorder_cancellation/',views.custorder_cancellation,name='custorder_cancellation'),
    path('cancel_order_customer/<str:order_number>/',views.cancel_order_customer,name='cancel_order_customer'),

    path('customer_my_returns/',views.customer_my_returns,name='customer_my_returns'),

    path('check/return_checklist/',views.return_check_mychecklist.as_view(),name='return_check_mychecklist'),
    path('return_counter_amount/<int:id>',views.return_counter_amount,name='return_counter_amount'),

    path('return_cust_accept_proposal/<int:id>',views.return_cust_accept_proposal,name='return_cust_accept_proposal'),
    path('close_window',views.close_window,name='close_window'),
    path('customer_return_continue/<int:id>',views.customer_return_continue,name='customer_return_continue'),
    path('cancel_request/<int:id>',views.cancel_request,name='cancel_request'),
    


]