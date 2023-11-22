from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from .models import Note, Chat, User_Chat, User, Message
from . import db
import json
import logging

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def homePage():
    # html that is being run on the page
    return render_template("homepage.html", user=current_user)

@views.route('/notes/', methods=['GET', 'POST'])
@login_required
def notes():      
    return render_template("notes.html", user=current_user)

@views.route('/chat/', methods=['GET'])
@login_required
def chat():
    chat_id = request.args.get('chat_id')
    if not chat_id:
        chat_id = -1
        
    print(f"chat_id: {chat_id}")
    
    query = text(f"""
    SELECT c.*
    FROM chat c
    JOIN user__chat uc
        ON c.id = uc.chat_id
    WHERE uc.user_id = {current_user.id}
    """)
    chats = db.session.execute(query)
    chats = [r for r in chats]


    return render_template("chat.html", user=current_user, chats=chats, chat_id=chat_id)


@views.route('/new-note/', methods=['POST'])
@login_required
def new_note():
    noteText = request.form.get('note')
    print(f"id= {request.args.get('chat_id')}")
    new_note = Note(data=noteText, user_id=current_user.id)
    
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('views.notes'))


@views.route('/send-chat/', methods=['POST'])
@login_required
def send_chat():
    messageText = request.form.get('message')
    chat_id = request.args.get('chat_id')
    new_message = Message(data=messageText, chat_id=chat_id, user_id=current_user.id)
    
    db.session.add(new_message)
    db.session.commit()
    print(url_for('views.chat'))
    return redirect(url_for('views.chat') + f"?chat_id={chat_id}")


@views.route('/new-chat/', methods=['POST'])
@login_required
def new_chat():
    username = request.form.get('chatUser')
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash("User does not exists", category='error')
        return redirect(url_for('views.chat'))
    
    if(user.id == current_user.id):
        flash("cannot create chat with self", category="error")
        return redirect(url_for('views.chat'))
    
    new_chat = Chat(name=f"{user.firstname} & {current_user.firstname}")
    db.session.add(new_chat)
    db.session.commit()
    
    new_userchat_relation = User_Chat(user_id=user.id, chat_id=new_chat.id)
    new_userchat_relation2 = User_Chat(user_id=current_user.id, chat_id=new_chat.id)
    db.session.add_all([new_chat, new_userchat_relation, new_userchat_relation2])
    db.session.commit()
    flash("chat created", category='success')

    return redirect(url_for('views.chat'))


@views.route('/delete-note/', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/load-messages/', methods=['GET'])
def loadMessages():
    chat_id = request.args.get('chat_id')
    messages = Message.query.filter_by(chat_id=chat_id).all()
    
    return jsonify([{'user_id': msg.user_id,  'data': msg.data} for msg in messages])


    
    

        
    

"""
# decorator sets this as root in website
@app.route("/")

    
    """