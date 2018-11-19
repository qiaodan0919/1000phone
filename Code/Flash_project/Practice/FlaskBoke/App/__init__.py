from flask import Flask
from App.ext import init_ext
from App.settings import envs
from App.api import init_api


def create_app(env):
    app = Flask(__name__, static_folder='../static')

    app.config.from_object(envs.get(env))
    init_ext(app)
    init_api(app)

    return app