from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from AXF.ext import db
from one.views_constant import ORDER_STATUS_NOT_PAY


class Main(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255))
    name = db.Column(db.String(16))
    trackid = db.Column(db.Integer, default=4)


class MainWheel(Main):
    __tablename__ = "axf_wheel"


class MainNav(Main):
    __tablename__ = 'axf_nav'


class MainMustBuy(Main):
    __tablename__ = 'axf_mustbuy'


class MainShop(Main):
    __tablename__ = 'axf_shop'


class MainShow(Main):
    __tablename__ = 'axf_mainshow'

    categoryid = db.Column(db.Integer, default=1)
    brandname = db.Column(db.String(64))
    img1 = db.Column(db.String(255))
    childcid1 = db.Column(db.Integer, default=1)
    productid1 = db.Column(db.Integer, default=1)
    longname1 = db.Column(db.String(128))
    price1 = db.Column(db.Float, default=1)
    marketprice1 = db.Column(db.Float, default=0)
    img2 = db.Column(db.String(255))
    childcid2 = db.Column(db.Integer, default=1)
    productid2 = db.Column(db.Integer, default=1)
    longname2 = db.Column(db.String(128))
    price2 = db.Column(db.Float, default=1)
    marketprice2 = db.Column(db.Float, default=0)
    img3 = db.Column(db.String(255))
    childcid3 = db.Column(db.Integer, default=1)
    productid3 = db.Column(db.Integer, default=1)
    longname3 = db.Column(db.String(128))
    price3 = db.Column(db.Float, default=1)
    marketprice3 = db.Column(db.Float, default=0)


class FoodType(db.Model):
    __tablename__ = 'axf_foodtype'

    id = db.Column(db.Integer, primary_key=True)
    typeid = db.Column(db.Integer, default=1)
    typename = db.Column(db.String(32))
    childtypenames = db.Column(db.String(255))
    typesort = db.Column(db.Integer, default=1)


class Goods(db.Model):
    __tablename__ = 'axf_goods'

    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.Integer, default=1)
    productimg = db.Column(db.String(255))
    productname = db.Column(db.String(128))
    productlongname = db.Column(db.String(255))
    isxf = db.Column(db.Boolean, default=False)
    pmdesc = db.Column(db.Boolean, default=False)
    specifics = db.Column(db.String(64))
    price = db.Column(db.Float, default=0)
    marketprice = db.Column(db.Float, default=1)
    categoryid = db.Column(db.Integer, default=1)
    childcid = db.Column(db.Integer, default=1)
    childcidname = db.Column(db.String(128))
    dealerid = db.Column(db.Integer, default=1)
    storenums = db.Column(db.Integer, default=1)
    productnum = db.Column(db.Integer, default=1)


class AXFUser(UserMixin, db.Model):
    __tablename__ = 'axf_user'

    id = db.Column(db.Integer, primary_key=True)

    u_username = db.Column(db.String(32), unique=True)
    _u_passwd = db.Column(db.String(255))
    u_email = db.Column(db.String(64), unique=True)
    u_icon = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise Exception("Error Action: Password can't be access")

    @password.setter
    def password(self, value):
        self._u_passwd = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self._u_passwd, value)


class Cart(db.Model):
    __tablename__ = 'axf_cart'

    id = db.Column(db.Integer, primary_key=True)

    c_user = db.Column(db.Integer, db.ForeignKey(AXFUser.id))
    c_goods = db.Column(db.Integer, db.ForeignKey(Goods.id))

    c_goods_num = db.Column(db.Integer, default=1)
    c_is_select = db.Column(db.Boolean, default=True)


class Order(db.Model):
    __tablename__ = 'axf_order'

    id = db.Column(db.Integer, primary_key=True)

    o_user = db.Column(db.Integer, db.ForeignKey(AXFUser.id))
    o_price = db.Column(db.Float, default=0)
    o_time = db.Column(db.DateTime, default=datetime.now)
    o_status = db.Column(db.Integer, default=ORDER_STATUS_NOT_PAY)


class OrderGoods(db.Model):
    __tablename__ = 'axf_ordergoods'

    id = db.Column(db.Integer, primary_key=True)

    o_order = db.Column(db.Integer, db.ForeignKey(Order.id))
    o_goods = db.Column(db.Integer, db.ForeignKey(Goods.id))
    o_goods_num = db.Column(db.Integer, default=1)






