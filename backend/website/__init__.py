from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import MetaData
from os import path
from flask_login import LoginManager
from flask_socketio import join_room, leave_room, send, SocketIO

app = Flask(__name__)   
db = SQLAlchemy()
socketio = SocketIO(app)
DB_NAME = "database.db"

def init_app():
    # create flask app and set key to prevent cookie tampering

    app.config['SECRET_KEY'] = "nC1imei3AdXpQAse61cyAWtYMfcmZvfePSkNiIqUguUeNlNe"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    # registers the pages configured in views/auth to the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note, Message, User_Chat, Chat
    
    with app.app_context():
        # db.drop_all()
        db.create_all()
        
        metadata_obj = MetaData()
        for t in metadata_obj.sorted_tables:
            print(t.name)
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app