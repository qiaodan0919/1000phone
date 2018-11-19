from flask_restful import Resource, reqparse, abort

from App.ext import db
from models.models import Student

parse = reqparse.RequestParser()
parse.add_argument('s_name', required=True, help='s_name is must')

class HelloResource(Resource):

    def post(self):
        args = parse.parse_args()
        s_name = args.get('s_name')
        student = Student()
        student.s_name = s_name
        if not student.save():
            abort(400, msg='not')
        return {'msg': 'Hello World'}