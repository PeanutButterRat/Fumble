import os.path
import configparser

from flask_socketio import SocketIO
from flask import Flask


socketio = SocketIO(asynch_mode='eventlet')
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.getcwd(), '.ini')))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=config['PROD']['DB_URI']
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    socketio.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

