from flask_restful import Api

from apis.cinema_admin.cinema_address_api import CinemaAddressesResource, CinemaAddressResource
from apis.cinema_admin.cinema_hall_api import CinemaHallsResource
from apis.cinema_admin.cinema_movie_api import CinemaMoviesResource
from apis.cinema_admin.cinema_movie_hall_api import CinemaMovieHallsResource
from apis.cinema_admin.cinema_user_api import CinemaUsersResource

cinema_client_api = Api(prefix='/cinema')

cinema_client_api.add_resource(CinemaUsersResource, '/users/')

cinema_client_api.add_resource(CinemaAddressesResource, '/addresses/')
cinema_client_api.add_resource(CinemaAddressResource, '/addresses/<int:id>/')

cinema_client_api.add_resource(CinemaMoviesResource, '/movies/')

cinema_client_api.add_resource(CinemaHallsResource, '/halls/')

cinema_client_api.add_resource(CinemaMovieHallsResource, '/moviehalls/')