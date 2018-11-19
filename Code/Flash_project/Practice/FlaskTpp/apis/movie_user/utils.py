from flask import request, abort, g

from App.ext import cache
from App.utils import MOVIE_USER
from apis.movie_user.model_utils import get_movie_user


def _verify():

    token = request.args.get("token")

    if not token:
        abort(401, msg="not login")

    if not token.startswith(MOVIE_USER):
        abort(403, msg='no access')

    user_id = cache.get(token)

    if not user_id:
        abort(401, msg="user not avaliable")

    user = get_movie_user(user_id)

    if not user:
        abort(401, msg="user not avaliable")

    g.user = user
    g.auth = token


def movie_users_login(fun):

    def wrapper(*args, **kwargs):

        _verify()

        return fun(*args, **kwargs)
    return wrapper


def movie_users_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(*args, **kwargs):

            _verify()

            if not g.user.check_permission(permission):
                abort(403, "user can't access")
            return fun(*args, **kwargs)
        return wrapper
    return require_permission_wrapper

