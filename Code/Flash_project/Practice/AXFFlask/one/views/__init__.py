from AXF.ext import login_manager
from one.models import AXFUser
from one.views.mainviews import blue
from one.views.serverviews import serverAction
from one.views.userviews import userAction


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(userAction)
    app.register_blueprint(serverAction)


@login_manager.user_loader
def load_user(id):
    return AXFUser.query.get(int(id))




