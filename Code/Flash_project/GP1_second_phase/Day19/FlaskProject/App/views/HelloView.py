import base64
import random

import os

import time
from flask import Blueprint, render_template, request, g, current_app, redirect, url_for, flash, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db, mail, cache
from App.models import News, Student
from App.settings import BASE_DIR
from App.utils import make_data_secret, send_verify_code

blue = Blueprint('blue', __name__)


@blue.route('/')
def index():
    return 'Index'


@blue.route('/addnews/')
def add_news():
    news = News()

    news.n_title = "周润发%d" % random.randrange(10000)
    news.n_content = "福利社会%d" % random.randrange(10000)

    db.session.add(news)
    db.session.commit()

    return 'Add Success'


@blue.route('/getnews/')
def get_news():

    news_list = News.query.all()

    news_content = render_template("news_content.html", news_list=news_list)

    # encode_content = base64.standard_b64encode(news_content.encode("utf-8")).decode("utf-8")
    #
    # print(encode_content)
    #
    # add_content_encode_content = "CHKa2GFL1twhMDhEZVfDfU2DoZHCLZk" + encode_content + "pOq3kRIxs26rmRtsUTJvBn9Z"
    #
    # print(add_content_encode_content)
    #
    # encode_content_twice = base64.standard_b64encode(add_content_encode_content.encode("utf-8")).decode("utf-8")
    #
    # print(encode_content_twice)

    encode_content_twice = make_data_secret(news_content)

    return render_template("NewsList.html", news_content=news_content, encode_content_twice=encode_content_twice)


@blue.route('/getshow/')
def get_show():

    t = request.args.get('t')

    print(t)

    c = time.time() * 1000

    print(c)

    try:

        t = int(t)
    except:
        return '2'

    if c > t and c - t < 1000:

        with open(os.path.join(BASE_DIR, 'App/static/js/show.js'), 'r') as file:

            js_content = file.read()

            # print(js_content)

        return js_content
    else:

        return '1%s' % g.msg


@blue.before_request
def before():

    print(request.url)

    g.msg = "呵呵哒"

    config = current_app.config

    print(config)

    keys = config.keys()

    for key in keys:
        print(key, config[key])

@blue.after_app_request
def after(resp):

    print('after')

    print(resp)

    print(type(resp))

    return resp


@blue.route('/student/register/', methods=["GET", "POST"])
def student_register():

    if request.method == "GET":
        return render_template('StudentRegister.html')

    elif request.method == "POST":
        username = request.form.get("username")

        password = request.form.get("password")

        phone = request.form.get("phone")

        # hash_pwd = generate_password_hash(password)
        code = request.form.get("code")

        cache_code = cache.get(username)

        if code != cache_code:
            return "验证失败"

        student = Student()

        student.s_name = username

        student.s_password = password

        student.s_phone = phone

        db.session.add(student)

        db.session.commit()

        return 'Register Success'


@blue.route('/student/login/', methods=["GET", "POST"])
def student_login():
    if request.method == "GET":
        return render_template('StudentLogin.html')

    elif request.method == "POST":
        username = request.form.get("username")

        password = request.form.get("password")

        student = Student.query.filter(Student.s_name.__eq__(username)).first()

        # if student and check_password_hash(student.s_password, password):
        if student and student.check_password(password):
            return 'Login Success'

        flash("用户名或密码错误")

        return redirect(url_for('blue.student_login'))


@blue.route('/sendmail/')
def send_mail():

    msg = Message("Flask Email", recipients=["rongjiawei1204@163.com",])

    msg.body = "哈哈  Flask 不过如此"

    msg.html = "<h2>你真是一个小天才</h2>"

    mail.send(message=msg)

    return '邮件发送成功'


@blue.route('/sendcode/')
def send_code():

    phone = request.args.get("phone")

    username = request.args.get("username")

    resp = send_verify_code(phone)

    result = resp.json()

    if result.get("code") == 200:
        obj = result.get("obj")

        cache.set(username, obj)

        data = {
            "msg": "ok",
            "status": 200
        }

        return jsonify(data)

    data = {
        "msg": "fail",
        "status": 400
    }

    return jsonify(data)