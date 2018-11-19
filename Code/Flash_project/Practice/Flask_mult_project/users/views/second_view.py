from flask import Blueprint, request, render_template, Response, session

second_view = Blueprint('second', '__name__')


@second_view.route('/secondindex/')
def index():
    return 'This is the second index!'


@second_view.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':

        username = request.form.get("username")

        response = Response("登录成功%s" % username)

        # response.set_cookie('username', username)
        session['username'] = username
        session['password'] = "110"

        return response


@second_view.route('/mine/')
def mine():
    username = session.get('username')

    return username