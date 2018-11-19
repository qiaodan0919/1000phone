from flask_restful import Resource, fields, reqparse, marshal_with, abort, marshal
from werkzeug.datastructures import FileStorage

from apis.admin.utils import admin_user_login
from apis.api_constant import HTTP_OK, HTTP_CREATE_OK
from apis.common.utils import filename_transfer
from models.common.movie_model import Movie

parse = reqparse.RequestParser()
parse.add_argument("showname", required=True, help="must supply showname")
parse.add_argument("shownameen", required=True, help="must supply shownameen")
parse.add_argument("director", required=True, help="must supply director")
parse.add_argument("leadingRole", required=True, help="must supply leadingRole")
parse.add_argument("type", required=True, help="must supply type")
parse.add_argument("country", required=True, help="must supply country")
parse.add_argument("language", required=True, help="must supply language")
parse.add_argument("duration", required=True, help="must supply duration")
parse.add_argument("screeningmodel", required=True, help="must supply screeningmodel")
parse.add_argument("openday", required=True, help="must supply openday")
parse.add_argument("backgroundpicture", type=FileStorage, required=True, help="must supply backgroundpicture", location=['files'])

movie_fields = {
    "showname": fields.String,
    "shownameen": fields.String,
    "director": fields.String,
    "leadingRole": fields.String,
    "type": fields.String,
    "country": fields.String,
    "language": fields.String,
    "duration": fields.Integer,
    "screeningmodel": fields.String,
    "openday": fields.DateTime,
    "backgroundpicture": fields.String,
}

multi_movies_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(movie_fields))
}


class MoviesResource(Resource):

    @marshal_with(multi_movies_fields)
    def get(self):
        movies = Movie.query.all()

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": movies
        }

        return data

    @admin_user_login
    def post(self):
        args = parse.parse_args()

        showname = args.get("showname")
        shownameen = args.get("shownameen")
        director = args.get("director")
        leadingRole = args.get("leadingRole")
        movie_type = args.get("type")
        country = args.get("country")
        language = args.get("language")
        duration = args.get("duration")
        screeningmodel = args.get("screeningmodel")
        openday = args.get("openday")
        backgroundpicture = args.get("backgroundpicture")

        # backgroundpicture = request.files.get("backgroundpicture")

        movie = Movie()
        movie.showname = showname
        movie.shownameen = shownameen
        movie.director = director
        movie.leadingRole = leadingRole
        movie.type = movie_type
        movie.country = country
        movie.language = language
        movie.duration = duration
        movie.screeningmodel = screeningmodel
        movie.openday = openday

        filepath, movie.backgroundpicture = filename_transfer(backgroundpicture.filename)
        backgroundpicture.save(filepath)


        if not movie.save():
            abort(400, msg="can't create movie")

        data = {
            "msg": "create success",
            "status": HTTP_CREATE_OK,
            "data": marshal(movie, movie_fields)
        }

        return data


class MovieResource(Resource):

    def get(self, id):
        return {"msg": "get ok"}

    @admin_user_login
    def patch(self, id):
        return {'msg': "patch ok"}

    @admin_user_login
    def put(self, id):
        return {'msg': "put ok"}

    @admin_user_login
    def delete(self, id):
        return {'msg': "delete ok"}