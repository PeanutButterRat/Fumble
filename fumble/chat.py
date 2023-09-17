from flask import (
    Blueprint, render_template, request, redirect, url_for, g
)
from flask_socketio import leave_room, join_room, rooms

from fumble.auth import login_required
from . import socketio

bp = Blueprint('chat', __name__)
available_rooms = set()


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'GET':
        return render_template('chat/index.html', rooms=list(available_rooms))

    return redirect(url_for('chat.join', room=request.form['room']))


@bp.route('/<string:room>', methods=('GET',))
@login_required
def join(room):
    if room is None:
        return redirect(url_for('chat.index'))

    return render_template('chat/room.html', room=room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']

    for r in rooms():
        leave_room(r)

    join_room(room)

    if room not in available_rooms:
        available_rooms.add(room)

    socketio.send(f'{username} has entered the room.', to=room)


@socketio.on('message')
def on_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    socketio.send(f'{username}: {message}', to=room)
