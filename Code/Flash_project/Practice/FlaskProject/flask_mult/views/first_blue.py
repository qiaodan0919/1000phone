from flask import Blueprint

from flask_mult.models import models, User

blue = Blueprint('blue', '__name__')


@blue.route('/')
def index():
    return '我是你爸爸!!!!'

@blue.route('/createdb/')
def createdb():
    models.create_all()

    return 'create success !!'

@blue.route('/adduser/')
def add_user():
    user = User()
    user.u_name = 'tom'

    user.save()
    return 'add success !!!'


@blue.route('/dropdb/')
def drop_db():
    models.drop_all()

    return 'drop success !!!'