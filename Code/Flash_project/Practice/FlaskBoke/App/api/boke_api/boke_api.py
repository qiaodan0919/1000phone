from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.api.use_api.utils import boke_users_login, boke_users_permission
from App.models.boke_model import BokeModel

boke_fields = {
    'b_title': fields.String,
    'b_content': fields.String,
    'b_user_id': fields.String,
}

parse = reqparse.RequestParser()
parse.add_argument("title", type=str)
parse.add_argument("content", type=str)

parse_put = reqparse.RequestParser()
parse_put.add_argument("id",required=True, help='请输入修改内容')
parse_put.add_argument("title", type=str)
parse_put.add_argument("content", type=str)




class BokeResource(Resource):

    @boke_users_login
    def post(self):
        args = parse.parse_args()
        title = args.get('title')
        content = args.get('content')

        boke = BokeModel()
        boke.b_title = title
        boke.b_content = content
        boke.b_user_id = g.user.id

        if not boke.save():
            abort(400, msg="create fail")

        data = {
            "status": 200,
            "msg": "博客创建成功",
            "data": marshal(boke, boke_fields)
        }

        return data

    @boke_users_login
    def put(self):
        args = parse_put.parse_args()
        title = args.get('title')
        content = args.get('content')
        id = args.get('id')

        boke = BokeModel.query.filter(BokeModel.b_user_id==g.user.id).filter(BokeModel.id==id).first()
        if not boke:
            abort(400, msg='博客不存在')

        boke.b_title = title or boke.b_title
        boke.b_content = content or boke.b_content

        if not boke.save():
            abort(400, msg="put fail")
        data = {
            "status": 200,
            "msg": "用户修改成功",
            "data": marshal(boke, boke_fields)
        }

        return data

class BokeDeleteResource(Resource):


    @boke_users_login
    def delete(self, id):
        boke = BokeModel.query.get(id)
        if not g.user.is_super:
            abort(400, msg='无权限')

        if not boke:
            abort(404, msg='博客不存在')

        if not boke.delete():
            abort(400, msg='无法删除')

        data = {
            "msg": "delete success",
            "status": 204
        }

        return data

