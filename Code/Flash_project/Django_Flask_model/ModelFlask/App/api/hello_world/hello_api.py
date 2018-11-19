from flask_restful import Resource

from App.ext import db


class HelloResource(Resource):

    def get(self):
        db.create_all()
        return {'msg': 'Hello World'}