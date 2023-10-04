from django.contrib import admin

from customers.models import Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('status','postal_code','address_line_1','unit_no','mobile')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Address,AddressAdmin)
