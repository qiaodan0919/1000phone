import os
import uuid

from flask import Blueprint, request, session, render_template, redirect, url_for
from flask_login import login_user, login_manager, logout_user

from AXF.config import SERVER_PORT, SERVER_HOST
from AXF.ext import db, cache, photos
from one.models import AXFUser
from one.view_helper import send_mail

userAction = Blueprint('userAction', __name__, url_prefix='/userAction')


@userAction.route('/login/', methods=["GET", "POST", "DELETE", "PUT", "PATCH"])
def login():
    if request.method == 'GET':
        error_message = session.get('error_message')
        data = {
            'title': '登录'
        }
        if error_message:
            del session['error_message']
            data['error_message'] = error_message
        return render_template('user/login.html', data=data)
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AXFUser.query.filter(AXFUser.u_username == username).first()
        if user and user.check_password(password):
            if user.is_active:
                login_user(user)
                session['user_id'] = user.id
                return redirect(url_for('axf.mine'))

            error = 'user not activate'
            return render_template('user/login.html', error=error)

        error = 'user does not exit or password wrong'
        return render_template('user/login.html', error=error)


@userAction.route('/register/', methods=["GET", "POST", "DELETE", "PUT", "PATCH"])
def register():
    if request.method == 'GET':
        data = {
            'title': '注册'
        }
        return render_template('user/register.html', data=data)

    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        icon = photos.save(request.files['icon'])
        pathname = os.path.join('/static/uploads/icons', icon)

        user = AXFUser()
        user.password = password
        user.u_username = username
        user.u_email = email

        user.u_icon = pathname

        db.session.add(user)
        db.session.commit()

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_mail(username, email, u_token)

        return redirect(url_for('userAction.login'))


@userAction.route('/activate/')
def activate():
    u_token = request.args.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        user = AXFUser.query.filter(AXFUser.id == user_id).first()
        user.is_active = True

        db.session.add(user)
        db.session.commit()
        cache.delete(u_token)
        return redirect(url_for('userAction.login'))


@userAction.route('/logout/')
def logout():
    session.pop('user_id')
    logout_user()
    return redirect(url_for('axf.mine'))



