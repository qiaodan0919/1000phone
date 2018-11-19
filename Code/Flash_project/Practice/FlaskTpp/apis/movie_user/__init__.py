from flask_restful import Api

from apis.movie_user.movie_hall_api import UserMovieHallsResource, UserMovieHallResource
from apis.movie_user.movie_order_api import MovieOrdersResource, MovieOrderResource
from apis.movie_user.movie_order_pay_api import MovieOrderPayResource
from apis.movie_user.movie_user_api import MovieUsersResource

client_api = Api(prefix='/user')

client_api.add_resource(MovieUsersResource, '/movieusers/')

client_api.add_resource(MovieOrdersResource, '/movieorders/')
client_api.add_resource(MovieOrderResource, '/movieorders/<int:order_id>/')

client_api.add_resource(UserMovieHallsResource, "/moviehalls/")
client_api.add_resource(UserMovieHallResource, "/moviehalls/<int:id>/")

client_api.add_resource(MovieOrderPayResource, "/orderpay/")