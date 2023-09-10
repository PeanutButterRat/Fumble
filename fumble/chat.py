from flask import (
    Blueprint, session, g, render_template, request, jsonify, flash, redirect, url_for
)

from fumble.auth import login_required
from fumble.db import db

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('chat/index.html')


@bp.route('/new', methods=('GET',))
@login_required
def new_chat():
    username = request.args.get('username', '')
    if not username:
        return f'Username required.', 400

    user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
    if user is None:
        return f'No user with name {username} exists!', 404

    names = sorted([g.user['username'], username])
    room = ''.join(names)

    return jsonify({
        'room': room,
    })


@bp.route('/usernames', methods=('GET',))
@login_required
def get_usernames():
    prefix = request.args.get('prefix', '')
    rows = db.execute("SELECT * FROM user WHERE username LIKE ? || '%'", (prefix,))
    usernames = [row['username'] for row in filter(lambda r: r['id'] != g.user['id'], rows)]

    return jsonify({'usernames': usernames})
