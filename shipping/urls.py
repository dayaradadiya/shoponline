from . import views
from django.urls import include, path
from accounts import views as AccountViews

urlpatterns = [
    

    path('shipping_data_toexcel/',views.shipping_data_toexcel,name='shipping_data_toexcel'),
]