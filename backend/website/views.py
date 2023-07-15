from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Message
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def homePage():
    # html that is being run on the page
    return render_template("homepage.html", user=current_user)

@views.route('/notes/', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        
        new_note = Message(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        
    return render_template("notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Message.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

"""
# decorator sets this as root in website
@app.route("/")

    
    """