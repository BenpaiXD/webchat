from website import init_app
from website.events import socketio


if __name__ == "__main__":
    # create instance of flask app
    app = init_app()    
    
    socketio.run(app)
    