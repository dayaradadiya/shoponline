from django.contrib import admin
from .models import Bank_Account_Info, BusinessProfile, ICProfile, User,UserProfile
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','role','is_active','is_staff')
    list_editable = ('is_active',)
    ordering = ('-date_joined',)
    list_filter = ('role',)
    fieldsets = ()

class BanklInfoAdmin(admin.ModelAdmin):
    list_display = ('user','bank_acc_holder_name','bank_name','branch_name')

admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(BusinessProfile)
admin.site.register(ICProfile)
admin.site.register(Bank_Account_Info,BanklInfoAdmin)
