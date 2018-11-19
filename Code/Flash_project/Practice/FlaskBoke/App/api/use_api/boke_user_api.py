import os

from flask import request, g, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.api.use_api.model_utils import get_boke_user
from App.api.use_api.utils import boke_users_login
from App.ext import photos, cache
from App.models.user_model import BokeUserModel
from App.utils import generate_boke_user_token, send_verify_code

parse_base = reqparse.RequestParser()
parse_base.add_argument('action', type=str, required=True, help='请确认请求参数')
parse_base.add_argument('password', type=str, required=True, help='请输入密码')

parse_register = parse_base.copy()
parse_register.add_argument('phone', type=str, required=True, help='请输入手机号码')
parse_register.add_argument('email', type=str, required=True, help='请输入邮箱')

parse_login = parse_base.copy()
parse_login.add_argument("email", type=str, required=True, help='请输入手机号码')
parse_login.add_argument("phone", type=str, required=True, help='请输入手机号码')
parse_login.add_argument("code", type=str, required=True, help='请输入验证码')

boke_user_fields = {
    'u_email': fields.String,
    'u_phone': fields.String,
    'password': fields.String(attribute="_password"),
}

single_boke_user_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(boke_user_fields)
}

class BokeUsersResource(Resource):

    def get(self):
        phone = request.args.get("phone")
        resp = send_verify_code(phone)
        result = resp.json()

        if result.get("code") == 200:
            obj = result.get("obj")
            cache.set(phone, obj)
            print(cache.get(phone))
            data = {
                "msg": "ok",
                "status": 200
            }

            return jsonify(data)

        data = {
            "msg": "fail",
            "status": 400
        }

        return jsonify(data)


    def post(self):
        args = parse_base.parse_args()
        action = args.get('action')
        password = args.get('password')
        if action == 'register':
            args_register = parse_register.parse_args()
            phone = args_register.get('phone')
            email = args_register.get('email')
            # icon = photos.save(request.files['icon'])
            # pathname = os.path.join('/static/uploads/icons', icon)

            boke_user = BokeUserModel()
            boke_user.u_email = email
            boke_user.u_phone = phone
            boke_user.password = password
            # boke_user.u_icon = pathname

            if not boke_user.save():
                abort(400, msg="create fail")

            data = {
                "status": 200,
                "msg": "用户创建成功",
                "data": boke_user
            }

            return marshal(data, single_boke_user_fields)

        elif action == 'login':
            args_login = parse_login.parse_args()

            email = args_login.get("email")
            phone = args_login.get("phone")
            code = args_login.get("code")

            user = get_boke_user(email) or get_boke_user(phone)
            print(cache.get(phone))

            if cache.get(phone) != code:
                abort(400, msg='验证码错误')

            if not user:
                abort(400, msg="用户不存在")

            if not user.check_password(password):
                abort(401, msg="密码错误")

            if user.is_delete:
                abort(401, msg="用户不存在")

            token = generate_boke_user_token()

            cache.set(token, user.id, timeout=60 * 60 * 24 * 7)

            data = {
                "msg": "login success",
                "status": 200,
                "token": token
            }

            return data

        else:
            abort(400, msg="其提供正确的参数")


parse_update = reqparse.RequestParser()
parse_update.add_argument("email", type=str)
parse_update.add_argument("phone", type=str)

class BokeUserActionResource(Resource):

    @boke_users_login
    def put(self):
        args = parse_update.parse_args()
        email = args.get("email")
        phone = args.get("phone")
        boke_user = g.user

        boke_user.u_email = email or boke_user.u_email
        boke_user.u_phone = phone or boke_user.u_phone

        if not boke_user.save():
            abort(400, msg="put fail")

        data = {
            "status": 200,
            "msg": "用户修改成功",
            "data": boke_user
        }

        return marshal(data, single_boke_user_fields)

class BokeUserdeleteResource(Resource):

    @boke_users_login
    def delete(self, id):
        boke_user = BokeUserModel.query.get(id)
        if not g.user.is_super:
            abort(400, msg='无权限')

        if not boke_user:
            abort(404, msg='用户不存在')
        boke_user.is_delete = True
        if not boke_user.save():
            abort(400, msg='无法删除')

        data = {
            "msg": "delete success",
            "status": 204
        }

        return data










