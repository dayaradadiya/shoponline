

/* Variables */

let chatName=''
let username=''
let chatSocket=null
let chatWindowUrl=window.location.href
let chatRoomUuid=Math.random().toString(36).slice(2,12)
var csrftoken = getCookie('csrftoken');
console.log('chatRoomUuid',chatRoomUuid)

/* Elements */

const chatElement  = document.querySelector('#chat')
const chatOpenElement  = document.querySelector('#chat_open')
const chatJoinElement  = document.querySelector('#chat_join')
const chatIconElement  = document.querySelector('#chat_icon')
const chatWelcomeElement  = document.querySelector('#chat_welcome')
const chatRoomElement  = document.querySelector('#chat_room')
const chatNameElement  = document.querySelector('#chat_name')
const chatLogElement  = document.querySelector('#chat_log')
const chatInputElement  = document.querySelector('#chat_message_input')
const chatSubmitElement  = document.querySelector('#chat_message_submit')
const chatSellerListElement  = document.querySelector('#list_seller')
const chatSellerNameElement  = document.querySelector('#user_name')


/* Functions*/
function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendMessage(){
    var message = chatInputElement.value
    
    chatSocket.send(JSON.stringify({
        'type' : 'message',
        'message' : message,
        'name' : chatName
    }))
    chatInputElement.value = ''
}

function onChatMessage(data){
    console.log('onChatMessage', data)
    let tmpInfo = document.querySelector('.tmp-info') 
    if (tmpInfo){
            tmpInfo.remove()
            }

    if (data.type == 'chat_message') {
        if (data.agent) {
            chatLogElement.innerHTML += `       
            <div class="chat-history">
                    <ul class="m-b-0">
                    <li class="clearfix">
                            <div class="message-data text-right">
                                    <span class="message-data-time">${data.created_at} ago </span>
                                    &nbsp;&nbsp;<div class="h-10 w-10 rounded-full text-center pt-2 float-right"><img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar"></div>
                            </div>
                            <div class="message other-message float-right"> ${data.message} </div>
                    </li>
                    </ul>
            </div>`  

        } else {
            chatLogElement.innerHTML += `   
            <div class="chat-history">
<ul class="m-b-0"> 
                        <li class="clearfix">
                            <div class="message-data">
                                <span class="message-data-time">${data.created_at} ago</span>
                            </div>
                            <div class="message my-message">${data.message}</div>                                    
                        </li>  </ul>
                        </div>
            `  
        }   
    } else if (data.type == 'users_update') {
        chatLogElement.innerHTML += `<p class="mt-2">The admin/agent has joined the chat!</p>`
    } else if (data.type == 'writing_active') {
        if (data.agent){
            let tmpInfo = document.querySelector('.tmp-info') 
            if (tmpInfo){
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `       
            <div class="tmp-info flex w-full mt-2 space-x-3 max-w-md"> 
                
                            <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                                <p class="text-sm">The agent/admin is writing a message</p>
                            </div>
                               <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                            </div>
            `  

        }}
        
    scrollToBottom()
}

async function joinChatRoom() {
    console.log('joined chatroom')
    
    chatName = chatNameElement.value

    console.log('joined as ',chatName)
    console.log('Room uuid ',chatRoomUuid)

    const data = new FormData()
    data.append('name',chatName)
    data.append('url',chatWindowUrl)
    

    await fetch(`/api/create-room/${chatRoomUuid}`,{
        method : 'POST',
        headers : {
            "X-CSRFToken" : csrftoken,
        },
        body : data
    })
    .then(function(res){
        return res.json()
    })
    .then(function(data){
        console.log('data',data)
    })

    // chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatRoomUuid}/`)

    chatSocket.onmessage = function(e){
        console.log('onMessage')
        onChatMessage(JSON.parse(e.data))
    }

    chatSocket.onopen = function(e){
        console.log('onOpen - chat socket was opened')

        scrollToBottom()
    }

    chatSocket.onclose = function(e){
        console.log('onClose - chat socket was closed')
    }

}



// async function joinSellerChatRoom() {
//     console.log('joined chatroom')
//     chatName = chatNameElement.value
//     username = chatSellerNameElement.value

//     console.log('joined as ',chatName)
//     console.log('Room uuid ',chatRoomUuid)

//     const data = new FormData()
//     data.append('name',chatName)
//     data.append('url',chatWindowUrl)
    

//     await fetch(`/api/create-room/${chatRoomUuid}`,{
//         method : 'POST',
//         headers : {
//             "X-CSRFToken" : csrftoken,
//         },
//         body : data
//     })
//     .then(function(res){
//         return res.json()
//     })
//     .then(function(data){
//         console.log('data',data)
//     })

//     chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/personal/${username}`)
//     // chatSocket = new WebSocket(`ws://${window.location.host}/ws/${window.location.pathname}/`)

//     chatSocket.onmessage = function(e){
//         console.log('onMessage')
//         onChatMessage(JSON.parse(e.data))
//     }

//     chatSocket.onopen = function(e){
//         console.log('onOpen - chat socket was opened')

//         scrollToBottom()
//     }

//     chatSocket.onclose = function(e){
//         console.log('onClose - chat socket was closed')
//     }

// }
/* Even listeners */

chatOpenElement.onclick = function(e){
    e.preventDefault()  

    chatIconElement.classList.add("hidden")
    chatWelcomeElement.classList.remove("hidden")

    return false
}

chatJoinElement.onclick = function(e){
    e.preventDefault()  

    chatWelcomeElement.classList.add("hidden")
    chatRoomElement.classList.remove("hidden")

    joinChatRoom()

    return false
}

    // chatSellerListElement.onclick = function(e){
    //     chatWelcomeElement.classList.add("hidden")
    //     chatRoomElement.classList.remove("hidden")

    //     joinSellerChatRoom()

    //     return false
    // }

chatSubmitElement.onclick = function(e){
    e.preventDefault()  

    sendMessage()
    return false
}

chatInputElement.onkeyup = function(e){
    if( e.keyCode == 13 ){
        sendMessage()
    }
}

chatInputElement.onfocus = function(e){
    chatSocket.send(JSON.stringify({
        'type':'update',
        'message' : 'writing_active',
        'name': chatName
    }))
}


/////////////////////////////////////////////

//consumer
/*

#daya  
 
class PersonnelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        me = self.scope['user']
        other_username = self.scope["url_route"]["kwargs"]["username"]
        other_user = User.objects.get(username=other_username)
        
        
        self.thread_obj = Thread.objects.get_or_create_personal_thread(me,other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'

        # self.user=self.scope['user']
        
        # Join room group
        # await self.get_room()
        await self.channel_layer.group_add(self.room_name,self.channel_name)
        print(f'[{self.channel_name}] -you r connected {self.room_name}')

        await self.accept()
        # inform user
        if self.user.is_staff:
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type' : 'users_update',
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        print(f'[{self.channel_name}] - disconnected -  {self.room_name} ')
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

        if not self.user.is_staff:
             await self.set_room_closed()
           
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        print(f'[{self.channel_name}] -received message - [{self.room_name}]- {text_data_json["message"]}')
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent','')
        username =  self.scope['user'].username


        if type == 'message':


            # msg = json.dumps({
            #         'text': event.get('text'),
            #         'username' : self.scope['user'].username
            #         }
            #      ) 

            # await self.create_message(event.get('text'))

            # #send message to group room
            # await self.channel_layer.group_send(
            #     self.room_name, {
            #       'type' : 'websocket.message',
            #       'text' : msg
            #     }
            # )
            new_message = await self.create_message(name,message,agent)          
            await self.channel_layer.group_send(
                            self.room_name, {
                                'type' : 'chat_message',
                                'message' : message,
                                'name' : name,
                                'agent' : agent,
                                'initials' : initials(name),
                                'created_at' :timesince(new_message.created_at),
                                'username' : username
                    }
                )
    async def chat_message(self,event):
        #send message to websocket front end
            print(f'[{self.channel_name}] -message sent -  {self.room_name} - {event["message"]}')
            await self.send(text_data=json.dumps({
                  'type': event['type'],
                    'message': event['message'] ,
					'name': event['name'],
                    'agent': event['agent'],
                    'initials': event['initials'],
                    'created_at': event['created_at'],
					'username' : self.scope['user'].username
					}))

    async def websocket_message(self,event):
        #send message to websocket front end
            print(f'[{self.channel_name}] -message sent -  {self.room_name} - {event["message"]}')
            await self.send({
                  'type': 'websocket.send',
                  'text' : event.get('text')
            })

    @database_sync_to_async
    def create_message(self,text):
         message = Message.objects.create(body=text,sent_by=self.scope['user'],thread=self.thread_obj)
        #  if agent :
        #       message.created_by = User.objects.get(pk=agent)
        #       message.save()
         message.save()

         self.room.messages.add(message)

         return message  
    # @sync_to_async 
    # def get_room(self):
    #      self.room = Room.objects.get(uuid=self.room_name) 
    '''
*/

/// routing.pt
//path('ws/chat/personal/<str:username>/',consumers.PersonnelConsumer.as_asgi()),

/* thread

# class TrackingModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True
    
# class Thread(TrackingModel):
#     THREAD_TYPE = (
#         ('personal', 'Personal'),
#         ('group', 'Group')
#     )

#     name = models.CharField(max_length=50, null=True, blank=True)
#     thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
#     users = models.ManyToManyField(User,blank=True,null=True)

#     objects = ThreadManager()

#     def __str__(self) -> str:
#         if self.thread_type == 'personal' and self.users.count() == 2:
#             return f'{self.users.first()} and {self.users.last()}'
#         return f'{self.name}'
*/