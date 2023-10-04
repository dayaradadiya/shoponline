

from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('bulk_product/',views.bulk_product,name='bulk_product'),

    path('generate/<str:file_name>',views.generate,name='generate'),

    path('download_basic_template/',views.download_basic_template,name='download_basic_template'),

    path('generate_subcat/',views.generate_subcat,name='generate_subcat'),

    path('generate_fourth_level_cat/',views.generate_fourth_level_cat,name='generate_fourth_level_cat'),
    


    path('bulk_category',views.bulk_category,name='bulk_category'),


   
]