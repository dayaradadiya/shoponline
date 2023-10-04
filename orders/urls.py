from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('place_order/',views.place_order, name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('tracker/',views.tracker,name='tracker'),

    path('order_complete_card/',views.order_complete_card,name='order_complete_card'),
    path('start_order/',views.start_order,name='start_order'),
    path('success/',views.success,name='success'),
    path('failed/',views.failed,name='failed'),
    path('edit_order_address/<int:pk>',views.edit_order_address,name='edit_order_address'),
    path('delete_order_address/<int:pk>',views.delete_order_address,name='delete_order_address'),
    path('add_order_address/',views.add_order_address,name='add_order_address'),
    

    # path('my_webhook/',views.my_webhook,name='my_webhook'),

    
]