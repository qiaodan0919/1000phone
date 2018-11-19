from flask import request, g
from flask_restful import abort

from App.ext import cache
from App.utils import ADMIN_USER
from apis.admin.model_utils import get_admin_user


def _verify():
    token = request.args.get("token")

    if not token:
        abort(401, msg="not login")

    if not token.startswith(ADMIN_USER):
        abort(403, msg='no access')

    user_id = cache.get(token)

    if not user_id:
        abort(401, msg="user not avaliable")

    user = get_admin_user(user_id)

    if not user:
        abort(401, msg="user not avaliable")

    g.user = user
    g.auth = token


def admin_user_login(fun):

    def wrapper(*args, **kwargs):

        _verify()

        return fun(*args,**kwargs)
    return wrapper


def admin_user_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(*args, **kwargs):

            _verify()

            if not g.user.check_permission(permission):
                abort(403, msg="user can't access")

            return fun(*args, **kwargs)
        return wrapper
    return require_permission_wrapper


