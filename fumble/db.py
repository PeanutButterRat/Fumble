from flask import g, current_app
from werkzeug.local import LocalProxy
from pymongo import MongoClient


def get_db():
    database = getattr(g, "_database", None)

    if database is None:
        client = MongoClient(current_app.config['MONGO_URI'])
        database = g._database = client['fumble']

    return database


db = LocalProxy(get_db)
