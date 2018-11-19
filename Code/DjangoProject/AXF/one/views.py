import re
import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from AXF.settings import MEDIA_KEY_PREFIX, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY, ALIPAY_APPID
from one.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods
from one.view_helper import sendemail_activate, get_total_price
from one.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_USER_OK, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND


def hello(request):
    return HttpResponse('Hello World!')


def home(request):

    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shop = MainShop.objects.all()

    main_shop0_1 = main_shop[0]
    main_shop1_3 = main_shop[1:3]
    main_shop3_7 = main_shop[3:7]
    main_shop7_11 = main_shop[7:11]

    main_shows = MainShow.objects.all()

    data = {
        'title': '首页',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows': main_shows,
    }
    return render(request, "main/home.html", context=data)


def market_with_params(request, typeid, childcid, order_rule):

    foodtypes = FoodType.objects.all()

    good_list = Goods.objects.all().filter(categoryid=typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        good_list = good_list.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        good_list = good_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        good_list = good_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        good_list = good_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        good_list = good_list.order_by("-productnum")

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]

    foodtype = foodtypes.filter(typeid=typeid).first()
    foodtypechildtypenames = foodtype.childtypenames
    typename_list = foodtypechildtypenames.split('#')
    typenamelist = [x.split(':') for x in typename_list]
    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'good_list': good_list,
        'typeid': int(typeid),
        'typenamelist': typenamelist,
        'childcid': childcid,
        'order_rule': order_rule,
        'order_rule_list': order_rule_list,
    }
    user_id = request.session.get('user_id')
    if user_id:
        data['is_login'] = True
        data['cart_list'] = Cart.objects.all()

    return render(request, 'main/market.html', context=data)


def market(request):
    return redirect(reverse('one:market_with_params', kwargs={
        'typeid': '104749',
        'childcid': '0',
        'order_rule': 0
    }))


def cart(request):

    Cart.objects.filter(c_goods_num=0).delete()

    carts = Cart.objects.filter(c_user=request.user)
    is_all_select = carts.filter(c_is_select=False).exists()
    data = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(request),
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '我的',
        'is_login': False,

    }
    if user_id:
        data['is_login'] = True
        user = AXFUser.objects.filter(pk=user_id).first()
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()
    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册'
        }
        return render(request, 'user/register.html',context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')
        password = make_password(password)

        user = AXFUser()
        user.u_username = username
        user.u_passwd = password
        user.u_email = email
        user.u_icon = icon
        user.save()

        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60*60*24)

        sendemail_activate(username, email, u_token)

        return redirect(reverse('one:login'))


def login(request):
    if request.method == 'GET':
        error_message = request.session.get('error_message')

        data = {
            'title': '登录'
        }
        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message
        return render(request, 'user/login.html', context=data)
    elif request.method == 'POST':

        username = request.POST.get('username')
        passwd = request.POST.get('password')

        user = AXFUser.objects.filter(u_username=username)
        if user.exists():
            user = user.first()
            if check_password(passwd, user.u_passwd):
                if user.is_active:
                    request.session['user_id'] = user.id
                    return redirect(reverse('one:mine'))
                request.session['error_message'] = 'user not activate'
                return redirect(reverse('one:login'))
            request.session['error_message'] = 'password wrong'
            return redirect(reverse('one:login'))
        request.session['error_message'] = 'user does not exit'
        return redirect(reverse('one:login'))


def logout(request):
    # request.session.flush()
    del request.session['user_id']
    return redirect(reverse('one:mine'))


def checkuser(request):

    username = request.GET.get('username')

    users = AXFUser.objects.filter(u_username=username)

    data = {
        'username_status': HTTP_USER_OK,
        'username_msg': 'user can use',

    }

    if users.exists():
        data['username_status'] = HTTP_USER_EXIST
        data['username_msg'] = 'user already exist'

    return JsonResponse(data=data)


def checkemail(request):
    email = request.GET.get('email')
    users = AXFUser.objects.filter(u_email=email)

    data = {
        'email_status': HTTP_USER_OK,
        'email_msg': 'email can use',
    }

    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'

    if (not(re.match(str, email))) or users.exists():
        data['email_status'] = HTTP_USER_EXIST
        data['email_msg'] = r"email doesn't use"

    return JsonResponse(data=data)


def activate(request):

    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        user = AXFUser.objects.filter(pk=user_id).first()
        user.is_active = True

        user.save()
        cache.delete(u_token)
        return redirect(reverse('one:login'))

    return HttpResponse('hahahaha')


def add_to_cart(request):

    goodid = request.GET.get('goodid')
    type = request.GET.get('type')
    cart = Cart.objects.filter(c_user=request.user).filter(c_goods=goodid)

    if cart.exists():
        cart_obj = cart.first()
        if type == 'add':
            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        elif type == 'sub' and cart_obj.c_goods_num > 0:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1

    else:
        if type == 'add':
            cart_obj = Cart()
            cart_obj.c_goods_id = goodid
            cart_obj.c_user = request.user
        elif type == 'sub':
            pass

    cart_obj.save()
    data = {
        'status': 200,
        'msg': 'add success',
        'c_good_num': cart_obj.c_goods_num,
    }

    return JsonResponse(data)


def change_cart_state(request):

    cart_id = request.GET.get('cartid')
    cart_obj = Cart.objects.filter(id=cart_id).first()
    cart_obj.c_is_select = not cart_obj.c_is_select
    cart_obj.save()
    carts = Cart.objects.filter(c_user=request.user)
    is_all_select = not carts.filter(c_is_select=False).exists()
    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(request),
    }
    return JsonResponse(data)


def change_shopping(request):
    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(id=cartid)
    type = request.GET.get('type')
    if type == 'sub':
        if cart_obj.c_goods_num > 0:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()
        else:
            cart_obj.delete()
    elif type == 'add':
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'goods_num': cart_obj.c_goods_num,
        'total_price': get_total_price(request),
    }

    return JsonResponse(data=data)


def all_select(request):
    cart_list = request.GET.get('cart_list').split('#')
    carts = Cart.objects.filter(id__in=cart_list)
    for cart in carts:
        cart.c_is_select = not cart.c_is_select
        cart.save()

    data = {
        'status': 200,
        'total_price': get_total_price(request),
    }

    return JsonResponse(data=data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user)

    order = Order()
    order.o_user = request.user
    order.o_price = get_total_price(request)
    order.save()

    carts_obj = carts.filter(c_is_select=True)
    for cart_obj in carts_obj:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        print(ordergoods)
        ordergoods.save()
        cart_obj.delete()

    data = {
        'status': 200,
        'msg': 'make orders',
        'order_id': order.id,

    }

    return JsonResponse(data=data)


def order_detail(request):

    order_id = request.GET.get('orderid')
    order = Order.objects.get(id=order_id)
    data = {
        'title': '订单详情',
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):

    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):

    order_id = request.GET.get('orderid')
    order = Order.objects.get(id=order_id)
    order.o_status = ORDER_STATUS_NOT_SEND
    order.save()

    data={
        'status': 200,
        'msg': 'payed'
    }

    return JsonResponse(data)


def alipay(request):

    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False  # 默认False
    )
    # 使用Alipay进行支付请求的发起

    subject = "20核系列 RTX80"

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no="110",
        total_amount=10000,
        subject=subject,
        return_url="http://www.1000phone.com",
        notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
    )

    return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)