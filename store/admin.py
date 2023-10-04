from django.contrib import admin
import admin_thumbnails
from .models import  Color, Contact,  Images,  Product, ProductGallery, ReviewRating, Size, Specification,     Variants, Variation

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class Variation_Admin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','variation_price','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','variation_price','is_active')


class ColorAdmin(admin.ModelAdmin):
    search_fields =  ['name']  
    list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    search_fields =  ['name'] 
    list_display = ['name','code']

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','variant_price','variant_stock','image_tag','variant_discount','variant_max_allowed_quantity']
    list_editable = ('product','color','size','variant_price','variant_stock','variant_discount','variant_max_allowed_quantity')

@admin_thumbnails.thumbnail('image')
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']


class Product_Admin(admin.ModelAdmin):
    list_display = ('product_name','weight','vendor','price','sub_category','section','is_available','brand','main_category','category','sub_category','image_tag','discount','max_allowed_quantity','is_active')
 
    readonly_fields = ('image_tag',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductGalleryInline,ProductImageInline,ProductVariantsInline]

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','timeStamp']
    search_fields =  ['name','email','subject']  
    list_per_page = 6      

admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Images,ImageAdmin)

admin.site.register(Product,Product_Admin)
admin.site.register(Variation,Variation_Admin)


admin.site.register(ReviewRating)

admin.site.register(ProductGallery)
admin.site.register(Contact,ContactAdmin)

# admin.site.register(Material)
# admin.site.register(Style)
# admin.site.register(Pattern)
# admin.site.register(StorageCapacity)
admin.site.register(Specification)

