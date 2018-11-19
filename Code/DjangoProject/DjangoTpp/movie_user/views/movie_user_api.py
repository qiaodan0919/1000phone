from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from DjangoTpp.utils import generate_movie_user_token
from api_constant import USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from movie_user.model_utils import get_movie_user
from movie_user.models import MovieUser
from movie_user.serializers import MovieUserSerializer


class MovieUsersApi(ListCreateAPIView):

    serializer_class = MovieUserSerializer
    queryset = MovieUser.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action').lower()

        if action == USER_ACTION_REGISTER:
            username = request.data.get('username')
            password = request.data.get('password')
            phone = request.data.get('phone')
            user = MovieUser()
            user.username = username
            user.password = password
            user.phone = phone
            user.save()
            user_serializer = MovieUserSerializer(user)

            return Response(data=user_serializer.data)
        elif action == USER_ACTION_LOGIN:
            username = request.data.get('username')
            password = request.data.get('password')
            phone = request.data.get('phone')

            user = get_movie_user(username) or get_movie_user(phone)

            if not user:
                raise exceptions.NotFound

            if not user.check_pass(password):
                raise exceptions.AuthenticationFailed

            if user.is_delete:
                raise exceptions.AuthenticationFailed

            token = generate_movie_user_token()

            cache.set(token, user.id)

            data = {
                "msg": "login success",
                "status": HTTP_OK,
                "token": token
            }
            return Response(data)


        else:
            raise exceptions.ValidationError
