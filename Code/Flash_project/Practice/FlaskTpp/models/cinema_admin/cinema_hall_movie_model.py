from App.ext import db
from models import BaseModel
from models.cinema_admin.cinema_hall_model import Hall
from models.common.movie_model import Movie


class HallMovie(BaseModel):

    h_movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))

    h_hall_id = db.Column(db.Integer, db.ForeignKey(Hall.id))

    h_time = db.Column(db.DateTime)
