

from django.contrib import admin
from customadmin import views

from customadmin.models import Mappings


# Register your models here.
class MappingsAdmin(admin.ModelAdmin):
    list_display = ('name','value')
 

admin.site.register(Mappings,MappingsAdmin)