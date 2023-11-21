#!usr/bin/python3
# -*- coding UTF-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__, static_url_path='/backend/static')
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
CORS(app, resources={r"/*": {"origins": "*", "methods": ["*"]}}, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', cors_allowed_headers='*', async_mode='threading')


from app import *

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
