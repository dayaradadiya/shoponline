# chat/consumers.py
import json

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from django.utils.timesince import timesince
from accounts.models import User
from chat.models import Message, Room
from chat.templatetags.chatextras import initials
from chat.views import get_order_vendors
from orders.models import Order
from channels.db import database_sync_to_async




class ChatConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f'chat_{self.room_name}'
        self.user=self.scope['user']

        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
            
        await self.accept()
        # inform user
        if self.user.is_staff:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type' : 'users_update',
                }
            )
        # await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type' : 'contacts',
        #         }
        #     )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

        await self.set_room_closed()
        # if not self.user.is_staff:
        #      await self.set_room_closed()
           
    async def receive(self,text_data):
        #receive message from websocket (front end)
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent','')


        if type == 'message':

            new_message = await self.create_message(name,message,agent)
            #send message to group room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type' : 'chat_message',
                    'message' : message,
                    'name' : name,
                    'agent' : agent,
                    'initials' : initials(name),
                    'created_at' :timesince(new_message.created_at)
                }
            )
        elif type == 'update' :
             #send update to the room
             await self.channel_layer.group_send(
                 self.room_group_name, {
                    'type' : 'writing_active',
                    'message' : message,
                    'name' : name,
                    'agent' : agent,
                    'initials' : initials(name),
                 })
            


    async def chat_message(self,event):
        #send message to websocket front end
            await self.send(text_data=json.dumps({
                  'type': event['type'],
                    'message': event['message'],
                    'name': event['name'],
                    'agent': event['agent'],
                    'initials': event['initials'],
                    'created_at': event['created_at'],
            }))

    async def writing_active(self,event):
        #  send writing is ctive to room
        await self.send(text_data=json.dumps({
                  'type': event['type'],
                    'message': event['message'],
                    'name': event['name'],
                    'agent': event['agent'],
                    'initials': event['initials'],
            }))


    async def users_update(self,event):
        #send information to websocket front end
            await self.send(text_data=json.dumps({
                  'type': 'users_update'
                  }))
    
    
    # getseller = get_seller(self.room_name)
    
          
    # async def contacts(self,event):
    #     getseller = await self.get_seller()
    #     await self.send(text_data=json.dumps({
    #                 'type' : 'contacts',
    #                 'vendor_name' : getseller
    #         }))

    @sync_to_async 
    def get_room(self):
         self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async        
    def get_seller(self):
               seller = get_order_vendors(self.user.id)
               return seller
    
    @sync_to_async
    def set_room_closed(self):
     self.room = Room.objects.get(uuid = self.room_name)
    #  self.room = await self.get_room()
     self.room.status = Room.CLOSED
     self.room.save()
   
    @sync_to_async
    def create_message(self,sent_by,message,agent):
         message = Message.objects.create(body=message,sent_by=sent_by)
         if agent :
              message.created_by = User.objects.get(pk=agent)
              message.save()

         self.room.messages.add(message)

         return message
    

#daya    
class vendorProduct(AsyncWebsocketConsumer):
    async def connect(self):
          self.room_name = self.scope['url_route']['kwargs']['id']
          self.room_group_name = f'vendor_{self.room_name}'
          self.user=self.scope['user']
          print('Connect')

          # Join room group
        #   await self.get_room()
          await self.channel_layer.group_add(self.room_group_name,self.channel_name)

          await self.accept()
          # inform user

          
          def get_seller(id):
               seller = get_order_vendors(id)
               return seller
          getseller = get_seller(self.room_name)
          
          await self.send(text_data=json.dumps({
               'type' : 'contacts',
                'vendor_name' : getseller,
          }))
               

     

    async def receive(self,text_data):
          self.channel_layer.group_send(
               self.room_group_name,
               {
                    'vendor_name' : text_data
               }
          )
    async def disconnect(self,close_code):
             # Leave room group
          await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

          await self.set_room_closed()
    @sync_to_async
    def set_room_closed(self):
        self.room = Room.objects.get(uuid = self.room_name)
        #  self.room = await self.get_room()
        self.room.status = Room.CLOSED
        self.room.save()