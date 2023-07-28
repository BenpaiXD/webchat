from flask import request
from . import socketio
from flask_socketio import join_room, leave_room, send, emit


@socketio.on("connect")
def connect():
    print(f"Connected to socket")
    
@socketio.on('joinChat')
def testevent(json):
    print(f"testevent: {str(json)}")