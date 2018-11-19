import os

from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={"CACHE_TYPE": "redis"})
mail = Mail()
photos = UploadSet('PHOTO')


def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app, db)
    cache.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)
