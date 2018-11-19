from flask import current_app
from flask_restful import Resource
from sqlalchemy import func

from App.ext import db
from App.models.cinema_admin.cinema_hall_movie_model import HallMovie
from App.models.common.movie_model import Movie
from App.models.movie_user.movie_order_model import MovieOrder


class MovieTopResource(Resource):

    def get(self):

        # Movie.query.get(2)

        results = db.session.query(Movie.id, Movie.showname, func.sum(MovieOrder.o_price)).join(Movie.hall_movies).join(HallMovie.h_orders).group_by(Movie.id).order_by(-func.sum(MovieOrder.o_price))

        print(type(results))

        print(results)

        for result in results:
            # print(result)

            current_app.logger.warning(result)

        # print(movie.hall_movies)

        data = {
            "msg": "ok"
        }

        return data