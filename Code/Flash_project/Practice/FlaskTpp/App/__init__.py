from flask import Flask

from App.ext import init_ext
from App.settings import envs
from apis import init_api


def create_app(env):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config.from_object(envs.get(env))
    init_ext(app)
    init_api(app)

    return app