from users.views.first_view import blue
from users.views.second_view import second_view


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(second_view)