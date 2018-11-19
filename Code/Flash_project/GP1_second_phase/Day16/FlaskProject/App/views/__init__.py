from App.views.third_blue import third
from .first_blue import blue
from .second_blue import second

# def init_route(app):
#
#     @app.route('/')
#     def hello_world():
#         return 'Hello World!'
#
#     @app.route('/hello/')
#     def hello():
#         return 'Hello 个鬼'
#
#     @app.route('/hi/')
#     def hi():
#         return 'Hi 什么?'


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(second)
    app.register_blueprint(third)

