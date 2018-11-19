from api.hello_world import hello_api


def init_api(app):
    hello_api.init_app(app)