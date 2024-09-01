import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from fumble.db import db

from pyotp import random_base32, totp

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                setup_key = random_base32()
                db.execute(
                    'INSERT INTO user (username, password, mfa_secret) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), setup_key),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                session['username'] = username
                session['mfa_secret'] = setup_key
                mfa_url = totp.TOTP(setup_key).provisioning_uri(name=username, issuer_name='Fumble')
                return render_template('mfa/setup.html', mfa_url=mfa_url, setup_key=setup_key)

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session['username'] = user['username']
            return redirect(url_for('auth.mfa'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/mfa', methods=('GET', 'POST'))
def mfa():
    if request.method == 'POST':
        if 'username' not in session:
            flash('User has not logged in.')
            return redirect(url_for('auth.login'))

        code = request.form['code']

        if not code:
            flash('Verification code is required.')
            return render_template('auth/challenge.html')

        matches, user = verify(code, session['username'])

        if matches:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash('Verification code does not match.')

    return render_template('mfa/challenge.html')


def verify(code, username):
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    secret_key = user['mfa_secret']

    return code == totp.TOTP(secret_key).now(), user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
