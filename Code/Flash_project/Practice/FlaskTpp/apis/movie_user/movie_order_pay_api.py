import uuid

from alipay import AliPay
from flask_restful import Resource, reqparse, abort

from App.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from apis.api_constant import HTTP_OK
from apis.movie_user.utils import movie_users_login
from models.movie_user.movie_order_model import MovieOrder

parse = reqparse.RequestParser()
parse.add_argument('order_id', required=True, help='请输入订单号')



class MovieOrderPayResource(Resource):

    @movie_users_login
    def post(self):
        args = parse.parse_args()
        order_id = args.get('order_id')
        movieorder = MovieOrder.query.filter(MovieOrder.id==order_id).first()

        if not movieorder:
            abort(400, msg='单号不存在')

        alipay_client = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=APP_PRIVATE_KEY,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA",  # RSA 或者 RSA2
            debug=False  # 默认False
        )

        subject = '淘票票单号' + order_id

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay_client.api_alipay_trade_page_pay(
            out_trade_no=uuid.uuid4().hex,
            total_amount=movieorder.o_price,
            subject=subject,
            return_url="http://www.1000phone.com",
            notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": {
                "pay_url": pay_url,
                "order_id": order_id
            }
        }

        return data

