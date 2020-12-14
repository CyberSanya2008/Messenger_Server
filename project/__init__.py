from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


db = SQLAlchemy()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    socketio.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
