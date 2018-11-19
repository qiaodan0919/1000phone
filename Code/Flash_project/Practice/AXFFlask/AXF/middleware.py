from flask import request, redirect, url_for
from flask_login import current_user

REQUIRE_LOGIN_NOMAL =[
    '/axf/cart/',
    '/axf/orderdetail/',
    '/axf/orderlistnotpay/',
]

REQUIRE_LOGIN_AJAX =[
    '/axf/addtocart/',
    '/axf/changecartstate/',
    '/axf/changeshopping/',
    '/axf/allselect/',
    '/axf/makeorder/',
]


def load_middleware(app):

    @app.before_request
    def LoginMiddleware():
        if request.path in REQUIRE_LOGIN_NOMAL:
            if not current_user.is_authenticated:
                print('====')
                return redirect(url_for('userAction.login'))

