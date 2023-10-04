from django.urls import path

from . import views

app_name='chat'

urlpatterns = [
    path("api/create-room/<str:uuid>", views.create_room, name="create_room"),
    path('chat-admin/',views.admin,name='admin'),
    path('chat-admin/add-user/',views.add_user,name='add_user'),
   
    path('chat-admin/users/<int:pk>',views.user_detail,name='user_detail'),
    path('chat-admin/users/<int:pk>/edit/',views.edit_user,name='edit_user'),

     path('chat-admin/<str:uuid>',views.room,name='room'),
    path('chat-admin/<str:uuid>/delete/',views.delete_room,name='delete_room'),
    path('api/ajaxlist/',views.ajaxlist,name='ajaxlist'),
]