from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from fumble.auth import login_required
from fumble.db import db

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('chat/index.html')


@bp.route('/new', methods=('POST',))
@login_required
def new():
    username = request.form['username']
    print(f'Creating chat with {username}')
    return redirect(url_for('blog.index'))


@bp.route('/usernames', methods=('GET',))
@login_required
def get_usernames():
    prefix = request.args.get('prefix', '')
    rows = db.execute("SELECT * FROM user WHERE username LIKE ? || '%'", (prefix,))
    usernames = [row['username'] for row in filter(lambda r: r['id'] != g.user['id'], rows)]

    return jsonify({'usernames': usernames})
