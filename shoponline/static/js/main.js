

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
const chatUserNameElement  = document.querySelector('#user_name')
const chatSellerListElement = document.querySelector('#list_seller')
var chatUserListElement  = document.querySelector('#user_list')


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

        }
    } else if (data.type == 'contacts') {
        for(let i = 0; i < data.length; i++) {
            obj = data[i]
            console.log('obj is :')
            console.log(obj)
            
            

            var msgListTag = document.createElement('li');
            // var imgTag = document.createElement('img');
            var pTag = document.createElement('p');

            pTag.textContent = obj.vendor_name;
            // imgTag.src = "https://bootdey.com/img/Content/avatar/avatar1.png";

            
            msgListTag.className = 'clearfix';
            

            // msgListTag.appendChild(imgTag);
            msgListTag.appendChild(pTag);
            document.querySelector('#list_user').appendChild(msgListTag);
       
    }
        
    }
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

    
    // var uname =  chatUserNameElement.value

    // var uname =  'daya radadiya'
    // await fetch(`/api/ajaxlist/`,{
    //         method : 'POST',
    //         headers : {
    //             "X-CSRFToken" : csrftoken,
    //         }
    //      }).then(function(res){
    //         return res.json()
    //     }).then(function(data){
    //         // for(let i = 0; i < data.length; i++) {
    //         //     obj = data[i]
    //         //contacts are : [{'model': 'chat.usercontacts', 'pk': 3, 'fields': {'user': 3, 'friends': [1, 2]}}]
    //         chatUserListElement += `<li class="clearfix">
    //         <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
    //         <div class="about">
    //             <p class="name" id="user_name">${data.fields}</p>
    //             <div class="status"> <i class="fa fa-circle offline"></i> left 7 mins ago </div>                                            
    //         </div>
    //     </li>`
            // }
        // })
    
    

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

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatRoomUuid}/`)

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

