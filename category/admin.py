
from django.contrib import admin

from .models import Category, Main_Category, Sub_Category, Fourth_Level_Category,Vendor_Category, Vendor_Main_Category, Vendor_Sub_Category

# Register your models here.

class Sub_Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','category')
    prepopulated_fields = {
        'slug':('name',)
        }

class Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','main_category')
    prepopulated_fields = {
        'slug':('name',)
        }
class Main_Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_editable = ('is_active',)
    list_display = ('name','is_active')
    prepopulated_fields = {
        'slug':('name',)
        }
class Fourth_Level_Category_Admin(admin.ModelAdmin):
    list_display = ('name','sub_category')
    search_fields = ['name']
    prepopulated_fields = {
        'slug':('name',)
        }
    
class Vendor_Sub_Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','vendor','category')
    prepopulated_fields = {
        'slug':('name',)
        }

class Vendor_Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','vendor','main_category')
    prepopulated_fields = {
        'slug':('name',)
        }
class Vendor_Main_Category_Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','vendor')
    prepopulated_fields = {
        'slug':('name',)
        }   


 
    
admin.site.register(Vendor_Main_Category,Vendor_Main_Category_Admin)
admin.site.register(Vendor_Category,Vendor_Category_Admin)
admin.site.register(Vendor_Sub_Category,Vendor_Sub_Category_Admin)

admin.site.register(Main_Category,Main_Category_Admin)
admin.site.register(Category,Category_Admin)
admin.site.register(Sub_Category,Sub_Category_Admin)

admin.site.register(Fourth_Level_Category,Fourth_Level_Category_Admin)


