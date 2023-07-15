from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def init_app():
    # create flask app and set key to prevent cookie tampering
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "nC1imei3AdXpQAse61cyAWtYMfcmZvfePSkNiIqUguUeNlNe"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    # registers the pages configured in views/auth to the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Message
    
    with app.app_context():
        # db.drop_all()
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app