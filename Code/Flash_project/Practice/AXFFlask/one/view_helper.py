from flask import render_template
from flask_mail import Message

from AXF.config import SERVER_HOST, SERVER_PORT
from AXF.ext import mail
from one.models import Cart


def send_mail(username, reveive, u_token):

    msg = Message('%s AXF Activate' % username, recipients=[reveive,])

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/userAction/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    html = render_template('user/activate.html', data=data)

    msg.html = html

    mail.send(message=msg)


def get_total_price(user_id):
    # carts = Cart.objects.filter(c_user=request.user)
    carts = Cart.query.filter(Cart.id == user_id)
    carts = carts.filter(Cart.c_is_select == True)
    total = 0
    for cart in carts:
        total = total + cart.c_goods_num * cart.c_goods.price

    return round(total, 2)