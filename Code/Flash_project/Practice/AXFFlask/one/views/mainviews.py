from flask import render_template, url_for, redirect, jsonify, Blueprint, request, session
from flask_login import login_required, current_user

from AXF.ext import db
from one.models import MainWheel, MainNav, MainMustBuy, MainShop, FoodType, Goods, MainShow, Cart, AXFUser, Order
from one.view_helper import get_total_price
from one.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    ORDER_STATUS_NOT_SEND, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_PAY

blue = Blueprint('axf', __name__, url_prefix='/axf')


@blue.route('/')
def index():
    return 'index'


@blue.route('/home/')
def home():
    main_wheels = MainWheel.query.filter()
    main_navs = MainNav.query.filter()
    main_mustbuys = MainMustBuy.query.filter()
    main_shop = MainShop.query.filter()

    main_shop0_1 = main_shop[0]
    main_shop1_3 = main_shop[1:3]
    main_shop3_7 = main_shop[3:7]
    main_shop7_11 = main_shop[7:11]

    main_shows = MainShow.query.filter()

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

    return render_template('main/home.html', data=data)


@blue.route('/market/')
def market():
    return redirect(url_for('axf.market_with_params', typeid='104749', childcid='0', order_rule='0'))


@blue.route('/market/<string:typeid>/<string:childcid>/<string:order_rule>/')
def market_with_params(typeid, childcid, order_rule):
    foodtypes = FoodType.query.filter()
    good_list = Goods.query.filter(Goods.categoryid == typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        good_list = good_list.filter(Goods.childcid == childcid)

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

    foodtype = foodtypes.filter(FoodType.typeid == typeid).first()
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
    return render_template('main/market.html', data=data)


@blue.route('/cart/')
def cart():
    cart = Cart.query.filter(Cart.c_goods_num == 0).first()
    if cart:
        db.session.delete(cart)
        db.session.commit()
    # carts = Cart.query.filter(Cart.c_user==request.user)
    carts = Cart.query.filter()
    if carts.filter(Cart.c_is_select == False):
        is_all_select = True
    else:
        is_all_select = False

    data = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(session.get('user_id')),
    }

    return render_template('main/cart.html', data=data)


@blue.route('/mine/')
def mine():
    user_id = session.get('user_id')
    data = {
        'title': '我的',
        'is_login': False,

    }
    print(session)

    if user_id:
        data['is_login'] = True
        user = AXFUser.query.filter(AXFUser.id == user_id).first()
        data['username'] = user.u_username
        data['icon'] = user.u_icon
        # data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_pay'] = Order.query.filter(Order.o_user == user_id).filter(Order.o_status == ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.query.filter(Order.o_user == user_id).filter(Order.o_status in [ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render_template('main/mine.html', data=data)