from django.contrib import admin

from chat.models import   Message, Room, UserContacts




admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserContacts)
