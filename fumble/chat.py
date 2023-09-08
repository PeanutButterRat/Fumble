from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from fumble.auth import login_required

bp = Blueprint('blog', __name__)


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


def get_users():
    pass
