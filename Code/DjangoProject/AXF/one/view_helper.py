from django.core.mail import send_mail
from django.template import loader

from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT
from one.models import Cart


def sendemail_activate(username, reveive, u_token):
    subject = '%s AXF Activate' % username
    message = 'xxxx'
    from_email = EMAIL_HOST_USER
    recipient_list = [reveive, ]

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/one/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)

    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email, recipient_list=recipient_list)


def get_total_price(request):
    carts = Cart.objects.filter(c_user=request.user)
    carts = carts.filter(c_is_select=True)
    total = 0
    for cart in carts:
        total = total + cart.c_goods_num * cart.c_goods.price

    return round(total, 2)