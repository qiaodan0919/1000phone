from flask import Blueprint, request, render_template, g, redirect, flash, url_for, abort

from App.ext import models, photos
from users.models import User

blue = Blueprint('blue', '__name__')


@blue.route('/')
def index():
    return render_template('hello.html')


@blue.route('/createdb/')
def createdb():
    models.create_all()

    return '创建成功'


@blue.route('/adduser/')
def add_user():
    user = User()
    user.u_name = 'tom'

    user.save()
    return 'add success !!!'


# @blue.route('/login/', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         print(request.form)
#         print(request.args)
#     elif request.method == 'GET':
#         print(request.values)
#
#     return 'yes'


# @blue.route('/login/', methods=['POST', 'GET'])
# def login():
#     print(request.form)
#     print(request.args)
#     return 'yes'

#原生办法实现
# @blue.route('/upload/', methods=['POST', 'GET'])
# def upload_file():
#     if request.method == 'GET':
#         return render_template('upload.html', title ='yonghu')
#     elif request.method == 'POST':
#         f = request.files['the_file']
#         f.save('/home/qiaodan/Flash_project/Practice/Flask_mult_project/App/static/file/user.jpg')
#     return 'yes'


@blue.route('/upload/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html', title ='yonghu')
    elif request.method == 'POST' and 'the_file' in request.files:
        filename = photos.save(request.files['the_file'])
        flash("Photo saved.")
        return 'success'




