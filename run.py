from os import getenv

from app import create_app
from app.socketio import socketio


app = create_app(getenv('FLASK_CONFIG'))

if __name__ == '__main__':
    socketio.run(app)
