from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    cache.init_app(app)