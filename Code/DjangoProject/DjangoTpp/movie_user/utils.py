from rest_framework import exceptions
from django.core.cache import cache

from DjangoTpp.utils import MOVIE_USER
from movie_user.model_utils import get_movie_user


def _verify(request):

    token = request.GET.get("token")
    if not token:
        raise exceptions.NotAuthenticated

    if not token.startswith(MOVIE_USER):
        raise exceptions.NotAuthenticated

    user_id = cache.get(token)
    print(user_id)
    if not user_id:
        raise exceptions.NotAuthenticated

    user = get_movie_user(user_id)

    if not user:
        raise exceptions.NotFound

    request.user = user


def movie_users_login(fun):

    def wrapper(self, request, *args, **kwargs):

        _verify(request)

        return fun(self, request, *args, **kwargs)
    return wrapper



def movie_users_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(self, request, *args, **kwargs):

            _verify(request)

            if not request.user.check_permission(permission):
                raise exceptions.AuthenticationFailed
            return fun(self, request, *args, **kwargs)
        return wrapper
    return require_permission_wrapper