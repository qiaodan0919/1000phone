from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from movie_user.models import VIP_USER
from movie_user.utils import movie_users_login, movie_users_permission


class MovieOrdersApi(ListCreateAPIView):
    @movie_users_login
    def post(self, request, *args, **kwargs):
        user = request.user
        data = {
            'msg': 'post order ok'
        }
        return Response(data)


class MovieOrderApi(RetrieveUpdateDestroyAPIView):
    @movie_users_permission(VIP_USER)
    def put(self, request, *args, **kwargs):
        data = {
            'msg': 'put order ok'
        }

        return Response(data)