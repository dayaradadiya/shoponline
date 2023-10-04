# chat/views.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from accounts.forms import AddUserForm, EditUserForm, UserForm
from django.contrib import messages
from accounts.models import User
from orders.models import Order
from vendor.models import Vendor
from .models import  Message, Room, UserContacts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.serializers import serialize
import json

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name','')
    url = request.POST.get('url','')

    Room.objects.create(uuid=uuid, client=name, url=url) 

    return JsonResponse({'message':'room created'})


@login_required
def admin(request):
     rooms = Room.objects.all()
     users = User.objects.filter(is_staff=True)

     context = {
          'rooms' : rooms,
          'users' : users,
     }
     return render(request,'chat/admin.html',context)

@login_required
def room(request,uuid):
     room=Room.objects.get(uuid=uuid)
     if room.status == Room.WAITING:
          room.status = Room.ACTIVE
          room.agent = request.user
          room.save() 

     return render(request, 'chat/room.html',{'room' : room})

@login_required
def add_user(request):

     if request.user.has_perm('user.add_user'):
          if request.method == 'POST':
               if form.is_valid():
                    user=form.save(commit=False)
                    user.is_staff=True
                    user.set_password(request.POST.get('password'))

                    if user.role == 'VENDOR':
                         group = Group.objects.get(name='vendor')
                         group.user_set.add(user)
                    messages.success(request,'The user was added!')
                    return redirect('/chat-admin/')
          else:
               form = AddUserForm()

          context = {
               'form' : form
          }

          return render(request,'chat/add_user.html',context)
     else:
          messages.error(request,"You do not have access to add users!")
          return redirect('/chat-admin/')
     
@login_required
def user_detail(request,pk):
     user = User.objects.get(pk=pk)
     rooms = user.rooms.all()
     context = {
          'user' : user,
          'rooms' : rooms,
     }

     return render(request,'chat/user_detail.html',context)

@login_required
def edit_user(request,pk):
     if request.user.has_perm('user.edit_user'):
          user = User.objects.get(pk=pk)
          if request.method == 'POST':
               form = EditUserForm(request.POST,  instance=user)

               if form.is_valid():
                    form.save()
               messages.success(request,'The changes was saved!')
               return redirect('/chat-admin/')
          else:
               form = EditUserForm(instance=user)
          context = {
               'form' : form,
               'user' : user,
          }

          return render(request,'chat/edit_user.html',context)

     else:     
          messages.error(request,"You do not have access to edit users!")
          return redirect('/chat-admin/')
     
@login_required
def delete_room(request,uuid):
     # if request.user.has_perm('room.delete_room'):
       room=Room.objects.get(uuid=uuid)

       room.delete()

     #   messages.error(request,"You do not have access to delete room!")
       return redirect('/chat-admin/') 
     # else :
     #     messages.error(request,"The room was deleted!")
     #     return redirect('/chat-admin/')  


     
def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return  Order.objects.filter(user__username=username).order_by("-created_at")[0]


def get_current_chat(id):
    return get_object_or_404(Message, id=id)

def get_order_vendors(id):
        if Order.objects.filter(user__id=id).exists():
            sellers =  Order.objects.filter(user__id=id).order_by("-created_at")[0]
            return sellers.order_placed_to()
        
       
def ajaxlist(request):
     # userlist=User.objects.filter(user=request.user)
     # print('userlist is :  return :' ,userlist)
     contacts = UserContacts.objects.filter(user__username = request.user.username)
     
     
     serialized_data = serialize("json", contacts)
     data = json.loads(serialized_data)
     
     context = {
            'data' :data,
        }
     
     return JsonResponse({'data':context})

     #    t = render_to_string('store/color_list.html', context=context) 
        # data = {'data' : render_to_string('store/color_list.html', context=context) }
        # data = {'rendered_table' : render_to_string('store/color_list.html', context=context) }
    
           