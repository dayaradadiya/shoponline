from . import views
from django.urls import include, path
from accounts import views as AccountViews

urlpatterns = [
    

    path('',AccountViews.vendorDashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('account/',views.vaccount,name='vaccount'),

    path('product-builder/',views.product_builder,name='product_builder'),
 
    #product CRUD
    path('add-product',views.add_product,name='add_product'),
    path('delete-product/<int:pk>/',views.delete_product,name='delete_product'),
    path('edit_product_main/<int:pk>/',views.edit_product_main,name='edit_product_main'),

    path('htmx/create_variant_form/',views.create_variant_form, name='create_variant_form'),
    path('htmx/detail_variant/<int:pk>',views.detail_variant, name='detail_variant'),
    path('edit_product/<int:pk>/',views.edit_product,name='edit_product'),
    path('htmx/detail_variant/<int:pk>/delete_variant/',views.delete_variant, name='delete_variant'),
    path('htmx/detail_variant/<int:pk>/update_variant/',views.update_variant, name='update_variant'),

    path('htmx/create_image_form/',views.create_image_form, name='create_image_form'),
    path('htmx/detail_image/<int:pk>',views.detail_image, name='detail_image'),
    path('edit_image/<int:pk>/',views.edit_image,name='edit_image'),
    path('htmx/detail_image/<int:pk>/delete_image/',views.delete_image, name='delete_image'),
    path('htmx/detail_image/<int:pk>/update_image/',views.update_image, name='update_image'),

    

    path('htmx/create_specn_form/<int:pk>',views.create_specn_form, name='create_specn_form'),
    path('htmx/detail_specn/<int:pk>',views.detail_specn, name='detail_specn'),
    path('edit_specn/<int:pk>/',views.edit_specn,name='edit_specn'),
    path('htmx/detail_specn/<int:pk>/delete_specn/',views.delete_specn, name='delete_specn'),
    path('htmx/detail_specn/<int:pk>/update_specn/',views.update_specn, name='update_specn'),


    path('delete-address/<int:pk>/',views.delete_vendor_address,name='delete_vendor_address'),
    path('edit_vendor_address/<int:pk>/',views.edit_vendor_address,name='edit_vendor_address'),
    

    path('htmx/detail_picture/<int:pk>',views.detail_picture, name='detail_picture'),

    path('order_details/<str:order_number>/',views.order_details,name='vendor_order_details'),
    path('my_orders/',views.my_orders,name='vendor_my_orders'),

    path('address/',views.address,name='vendor_address'),
    path('category_module/',views.category_module,name='category_module'),
    path('sub_category_module/',views.sub_category_module,name='sub_category_module'),
    path('fourth_level_category_module/',views.fourth_level_category_module,name='fourth_level_category_module'),
    path('fifth_level_category_module/',views.fifth_level_category_module,name='fifth_level_category_module'),
    

    path('order_pdf/<str:order_number>/<int:id>',views.order_pdf.as_view(),name='order_pdf'),
    path('download_pdf/<str:order_number>/<int:id>',views.download_pdf.as_view(),name='download_pdf'),
    
    path('check/checklist/',views.check_mychecklist.as_view(),name='check_mychecklist'),
    
    path('readytoship/<str:order_number>/<int:id>',views.readytoship,name='readytoship'),
    path('mass_readytoship/',views.mass_readytoship,name='mass_readytoship'),

    path('cancel_item_vendor/<str:order_number>/<int:id>',views.cancel_item_vendor,name='cancel_item_vendor'),
    path('request_extension/<str:order_number>/<int:id>',views.request_extension,name='request_extension'),

    path('item_shipped/<str:order_number>/<int:id>',views.item_shipped,name='item_shipped'),
    path('shipped_in_bulk/',views.shipped_in_bulk,name='shipped_in_bulk'),
    
    path('orders_overview/',views.orders_overview,name='orders_overview'),
    # path('order_pdf_bulk/',views.order_pdf_bulk.as_view(),name='order_pdf_bulk'),
    
    path('vendorder_cancellation/',views.vendorder_cancellation,name='vendorder_cancellation'),
    path('cancel_order_vendor/<str:order_number>/',views.cancel_order_vendor,name='cancel_order_vendor'),

    path('return_orders/',views.return_orders,name='return_orders'),

    path('approve_return/<int:id>',views.approve_return,name='approve_return'),
    
    path('return_partial_amount/<int:id>',views.return_partial_amount,name='return_partial_amount'),
    path('return_seller_accept_proposal/<int:id>',views.return_seller_accept_proposal,name='return_seller_accept_proposal'),
    
    path('close_window_selr/',views.close_window_selr,name='close_window_selr'),

    path('return_full_refund/<int:id>',views.return_full_refund,name='return_full_refund'),
    path('approvalof_seller_proposal_acceped/<int:id>',views.approvalof_seller_proposal_acceped,name='approvalof_seller_proposal_acceped'),
    path('seller_dispute/<int:id>',views.seller_dispute,name='seller_dispute'),
    path('upload_evidence/<int:id>',views.upload_evidence,name='upload_evidence'),
    path('reject_straight/<int:id>',views.reject_straight,name='reject_straight'),
    path('full_refund_noreturn/<int:id>',views.full_refund_noreturn,name='full_refund_noreturn'),

    
    path('vendor_my_returns/',views.vendor_my_returns,name='vendor_my_returns'),
    path('check/return_back_checklist/',views.returnback_check_mychecklist.as_view(),name='returnback_check_mychecklist'),
    


    path('vendor_maincategory/',views.vendor_maincategory,name='vendor_maincategory'),
    path('vendor_cat/',views.vendor_cat,name='vendor_cat'),
    path('vendor_subcategory/',views.vendor_subcategory,name='vendor_subcategory'),

    path('products_by_maincategory/<int:pk>',views.products_by_maincategory,name='products_by_maincategory'),
    path('products_by_cat/<int:pk>',views.products_by_cat,name='products_by_cat'),
    path('products_by_subcategory/<int:pk>',views.products_by_subcategory,name='products_by_subcategory'),



    path('add_main_category/',views.add_main_category,name='add_main_category'),
    path('edit_main_category/<int:pk>',views.edit_main_category,name='edit_main_category'),
    path('delete_main_category/<int:pk>',views.delete_main_category,name='delete_main_category'),

    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:pk>',views.edit_category,name='edit_category'),
    path('delete_category/<int:pk>',views.delete_category,name='delete_category'),

    path('add_sub_category/',views.add_sub_category,name='add_sub_category'),
    path('edit_sub_category/<int:pk>',views.edit_sub_category,name='edit_sub_category'),
    path('delete_sub_category/<int:pk>',views.delete_sub_category,name='delete_sub_category'),

    path('vend_category_module/',views.vend_category_module,name='vend_category_module'),
    path('vendor_balance/',views.vendor_balance,name='vendor_balance'),
    
     
]