import os

from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads

models = SQLAlchemy()
migrate = Migrate()
photos = UploadSet('PHOTO')


def init_ext(app):
    models.init_app(app=app)
    migrate.init_app(app, models)
    configure_uploads(app, photos)
    Session(app)
