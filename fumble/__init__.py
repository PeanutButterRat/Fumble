import os.path

from flask_socketio import SocketIO
from flask import Flask
from flask_qrcode import QRcode


socketio = SocketIO(asynch_mode='eventlet')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fumble.sqlite')
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
    QRcode(app)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')

    return app
