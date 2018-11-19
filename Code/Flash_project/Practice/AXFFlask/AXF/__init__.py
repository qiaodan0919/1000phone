from flask import Flask

from AXF.ext import init_ext
from AXF.middleware import load_middleware
from AXF.settings import envs
from one.views import init_view


def create_app(env):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(envs.get(env))

    init_ext(app)
    init_view(app)

    load_middleware(app)

    return app