from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from one.models import AXFUser

REQUIRE_LOGIN_NOMAL =[
    '/one/cart/',
    '/one/orderdetail/',
    '/one/orderlistnotpay/',
]

REQUIRE_LOGIN_AJAX =[
    '/one/addtocart/',
    '/one/changecartstate/',
    '/one/changeshopping/',
    '/one/allselect/',
    '/one/makeorder/',
]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self,requset):

        if requset.path in REQUIRE_LOGIN_AJAX:
            user_id = requset.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(id=user_id)
                    requset.user = user
                except:
                    data = {
                        'status': 301,
                        'msg': 'user not avaliable'
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'status': 301,
                    'msg': 'user mot login'
                }
                return JsonResponse(data)

        if requset.path in REQUIRE_LOGIN_NOMAL:
            user_id = requset.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(id=user_id)
                    requset.user = user
                except:
                    return redirect(reverse('one:login'))
            else:
                return redirect(reverse('one:login'))
