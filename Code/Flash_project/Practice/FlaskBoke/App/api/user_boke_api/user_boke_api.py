from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.api.use_api.utils import boke_users_login
from App.models.boke_user_model import UserBokeModel

parse_post = reqparse.RequestParser()
parse_post.add_argument('boke_id', type=str, required=True, help='请输入博客id')

boke_fields = {
    'id': fields.String,
    'b_boke_id': fields.String,
}

user_fields = {
    'b_user_id': fields.String,
}

multi_user_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(user_fields))
}

multi_boke_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(boke_fields))
}

class UserBokeResource(Resource):

    @boke_users_login
    def post(self):
        args = parse_post.parse_args()
        boke_id = args.get('boke_id')
        print(boke_id)
        user_id = g.user.id

        # boke_user_exit = UserBokeModel.query.fliter(UserBokeModel.b_boke_id==boke_id).first()
        # if not boke_user_exit:
        #     abort(400, msg='不存在这个博客')

        boke_user = UserBokeModel()
        boke_user.b_user_id = user_id
        boke_user.b_boke_id = int(boke_id)

        if not boke_user.save():
            abort(400, msg='存储失败')

        data = {
            "status": 200,
            "msg": "收藏创建成功",
            "data": marshal(boke_user, boke_fields)
        }

        return data


class UserAllBokeResource(Resource):

    def post(self, id):

        user_list = UserBokeModel.query.filter(UserBokeModel.b_boke_id==id)

        data = {
            "status": 200,
            "msg": "查询创建成功",
            "data": user_list
        }

        return marshal(data, multi_user_fields)


class BokeAllUserResource(Resource):

    def post(self, id):
        boke_list = UserBokeModel.query.filter(UserBokeModel.b_user_id==id)

        data = {
            "status": 200,
            "msg": "查询创建成功",
            "data": boke_list
        }

        return marshal(data, multi_boke_fields)