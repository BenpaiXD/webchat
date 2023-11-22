from flask import request
from flask_login import current_user
from flask_socketio import join_room, leave_room, send, emit
from . import socketio, db, clients
from .models import Message, User, Chat, User_Chat
import json


@socketio.on("connect")
def connect(auth):
    print(f" user {current_user.firstname} has connected to socket")
    print(f"sid: {request.sid}")
    clients[current_user.id] = request.sid
    

@socketio.on("disconnect")
def disconnect():
    print(f"user {current_user.firstname} has disconnected from the socket")
    
@socketio.on('joinChat')
def joinChat(JSON):
    chat_id = JSON['chat_id']
    
    join_room(chat_id)
    print(f"joined room {chat_id}")
    
    
@socketio.on('sendMessage')
def sendMessage(data):
    print(f"data: {data}")
    
    content = {'user_name': current_user.firstname, 'user_id': current_user.id, 'message': data['data']}
    
    send(content, to=data['chat_id'])
    
    
    new_message = Message(data=data['data'], chat_id=data['chat_id'], user_id=current_user.id)
    db.session.add(new_message)
    db.session.commit()
    print(f"message sent in chat {data['chat_id']}")



@socketio.on('new-chat')
def newChat(data):
    username = data['username']
    currUserID = int(data['currentUserID'])
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return
    if(user.id == current_user.id):
        return

    new_chat = Chat(name=f"{user.firstname} & {current_user.firstname}")
    db.session.add(new_chat)
    db.session.commit()
    
    new_userchat_relation = User_Chat(user_id=user.id, chat_id=new_chat.id)
    new_userchat_relation2 = User_Chat(user_id=current_user.id, chat_id=new_chat.id)
    db.session.add_all([new_chat, new_userchat_relation, new_userchat_relation2])
    db.session.commit()   
    
    content = {
        'id': new_chat.id,
        'name': new_chat.name
    } 
    
    join_room(clients[currUserID])
    emit("chat-created", content)