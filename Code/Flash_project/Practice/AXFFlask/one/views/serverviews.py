import re

from flask import Blueprint, request, jsonify

from one.models import AXFUser
from one.views_constant import HTTP_USER_OK, HTTP_USER_EXIST

serverAction = Blueprint('serverAction', __name__, url_prefix='/serverAction')


@serverAction.route('/checkuser/')
def checkuser():
    username = request.args.get('username')
    user = AXFUser.query.filter(AXFUser.u_username == username).first()

    data = {
        'username_status': HTTP_USER_OK,
        'username_msg': 'user can use',
    }
    if user:
        data['username_status'] = HTTP_USER_EXIST
        data['username_msg'] = 'user already exist'

    return jsonify(data)


@serverAction.route('/checkemail/')
def checkemail():
    email = request.args.get('email')
    users = AXFUser.query.filter(AXFUser.u_email == email).first()
    print(email)
    data = {
        'email_status': HTTP_USER_OK,
        'email_msg': 'email can use',
    }

    # str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    str = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
    print(not (re.match(str, email)))
    print(users)
    if (not (re.match(str, email))) or users:
        data['email_status'] = HTTP_USER_EXIST
        data['email_msg'] = r"email doesn't use"

    return jsonify(data)