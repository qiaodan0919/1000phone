from flask_restful import Resource


class UsersResource(Resource):

    def get(self):
        return {"msg": "users list"}


class UserResource(Resource):

    def get(self, id):
        return {"msg": "user%d ok" % id}