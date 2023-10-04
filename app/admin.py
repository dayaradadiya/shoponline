from django.contrib import admin

from app.models import Brand, Section



class BrandAdmin(admin.ModelAdmin):
    search_fields =  ['name']  

# Register your models here.
admin.site.register(Brand,BrandAdmin)
admin.site.register(Section)