from flask import Blueprint

second = Blueprint('second', '__name__')


@second.route('/qiao/')
def index():
    return '我是你zuiaide爸爸!!!!'