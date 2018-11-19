from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads


db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
cache = Cache(config={'CACHE_TYPE': 'redis'})
sess = Session()
mail = Mail()
photos = UploadSet('PHOTO')
login_manager = LoginManager()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    # toolbar.init_app(app)
    cache.init_app(app)
    sess.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)
    login_manager.init_app(app)

