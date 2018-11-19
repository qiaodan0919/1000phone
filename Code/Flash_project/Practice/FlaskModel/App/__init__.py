from flask import Flask

from App.ext import init_ext
from App.settings import envs
from one.views import init_view


def create_app(env):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.debug = True
    app.config.from_object(envs.get(env))
    init_ext(app)
    init_view(app)

    return app