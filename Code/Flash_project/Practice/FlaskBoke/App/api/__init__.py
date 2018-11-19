from App.api.boke_api import boke_api
from App.api.use_api import user_api
from App.api.user_boke_api import userboke_api


def init_api(app):
    user_api.init_app(app)
    boke_api.init_app(app)
    userboke_api.init_app(app)